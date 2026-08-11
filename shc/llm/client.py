"""OpenRouter LLM client with disk cache and cost accounting.

Provides multi-model routing via OpenRouter's unified API. All calls are
cached to disk keyed by SHA256(model + messages + params) so sweeps can
be re-run without cost.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Cache directory
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / ".cache" / "llm"

# OpenRouter API endpoint
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# Known model pricing (input $/1M tokens, output $/1M tokens)
# Updated periodically - costs are also returned by OpenRouter in response
MODEL_PRICING: dict[str, tuple[float, float]] = {
    "anthropic/claude-sonnet-4-20250514": (3.0, 15.0),
    "anthropic/claude-3.5-sonnet": (3.0, 15.0),
    "anthropic/claude-3-haiku": (0.25, 1.25),
    "openai/gpt-4o": (2.5, 10.0),
    "openai/gpt-4o-mini": (0.15, 0.6),
    "openai/o3-mini": (1.1, 4.4),
    "google/gemini-2.5-flash-preview": (0.15, 0.6),
    "google/gemini-2.5-pro-preview": (1.25, 10.0),
    "deepseek/deepseek-chat": (0.14, 0.28),
    "deepseek/deepseek-coder": (0.14, 0.28),
    "meta-llama/llama-3.1-70b-instruct": (0.52, 0.75),
    "meta-llama/llama-3.1-405b-instruct": (2.0, 2.0),
    "qwen/qwen-2.5-coder-32b-instruct": (0.2, 0.2),
}


@dataclass
class LLMResponse:
    """Structured response from an LLM call."""

    content: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    latency_s: float = 0.0
    cached: bool = False
    finish_reason: str = ""
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """A single message in a conversation."""

    role: str  # "system", "user", "assistant"
    content: str


def _cache_key(model: str, messages: list[Message], params: dict[str, Any]) -> str:
    """Compute SHA256 cache key from model + messages + params."""
    payload = {
        "model": model,
        "messages": [{"role": m.role, "content": m.content} for m in messages],
        "params": params,
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def _cache_path(key: str) -> Path:
    """Get the file path for a cache entry."""
    # Use first 2 chars as subdirectory for filesystem efficiency
    return CACHE_DIR / key[:2] / f"{key}.json"


def _read_cache(key: str) -> dict[str, Any] | None:
    """Read a cached response, or None if miss."""
    path = _cache_path(key)
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
    return None


def _write_cache(key: str, data: dict[str, Any]) -> None:
    """Write a response to the disk cache."""
    path = _cache_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _compute_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Compute cost in USD from token counts and model pricing."""
    pricing = MODEL_PRICING.get(model)
    if pricing is None:
        # Unknown model - estimate conservatively
        return (prompt_tokens * 2.0 + completion_tokens * 10.0) / 1_000_000
    input_rate, output_rate = pricing
    return (prompt_tokens * input_rate + completion_tokens * output_rate) / 1_000_000


class LLMClient:
    """Multi-model LLM client with caching and cost tracking.

    Usage:
        client = LLMClient()
        response = client.generate(
            model="anthropic/claude-sonnet-4-20250514",
            messages=[Message(role="user", content="Write a function...")],
        )
        print(response.content, response.cost_usd)
    """

    def __init__(
        self,
        api_key: str | None = None,
        cache_dir: Path | None = None,
        enable_cache: bool = True,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.cache_dir = cache_dir or CACHE_DIR
        self.enable_cache = enable_cache
        self._total_cost = 0.0
        self._total_prompt_tokens = 0
        self._total_completion_tokens = 0
        self._call_count = 0
        self._cache_hits = 0

    @property
    def total_cost(self) -> float:
        return self._total_cost

    @property
    def total_tokens(self) -> int:
        return self._total_prompt_tokens + self._total_completion_tokens

    @property
    def stats(self) -> dict[str, Any]:
        """Return current session statistics."""
        return {
            "total_cost_usd": self._total_cost,
            "total_prompt_tokens": self._total_prompt_tokens,
            "total_completion_tokens": self._total_completion_tokens,
            "total_calls": self._call_count,
            "cache_hits": self._cache_hits,
            "cache_hit_rate": (
                self._cache_hits / self._call_count if self._call_count > 0 else 0.0
            ),
        }

    def generate(
        self,
        model: str,
        messages: list[Message],
        temperature: float = 0.0,
        max_tokens: int = 4096,
        stop: list[str] | None = None,
        seed: int | None = None,
    ) -> LLMResponse:
        """Generate a completion from the specified model.

        Args:
            model: OpenRouter model identifier (e.g. "anthropic/claude-sonnet-4-20250514")
            messages: conversation history
            temperature: sampling temperature (0.0 for deterministic)
            max_tokens: max completion tokens
            stop: optional stop sequences
            seed: optional seed for reproducibility

        Returns:
            LLMResponse with content, tokens, cost, latency
        """
        self._call_count += 1

        # Build params dict for caching
        params: dict[str, Any] = {
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if stop:
            params["stop"] = stop
        if seed is not None:
            params["seed"] = seed

        # Check cache
        if self.enable_cache:
            key = _cache_key(model, messages, params)
            cached = _read_cache(key)
            if cached is not None:
                self._cache_hits += 1
                response = LLMResponse(
                    content=cached["content"],
                    model=cached.get("model", model),
                    prompt_tokens=cached.get("prompt_tokens", 0),
                    completion_tokens=cached.get("completion_tokens", 0),
                    total_tokens=cached.get("total_tokens", 0),
                    cost_usd=cached.get("cost_usd", 0.0),
                    latency_s=0.0,
                    cached=True,
                    finish_reason=cached.get("finish_reason", ""),
                )
                self._total_cost += response.cost_usd
                self._total_prompt_tokens += response.prompt_tokens
                self._total_completion_tokens += response.completion_tokens
                return response

        # Make the API call
        response = self._call_api(model, messages, params)

        # Cache the response
        if self.enable_cache:
            _write_cache(key, {
                "content": response.content,
                "model": response.model,
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
                "cost_usd": response.cost_usd,
                "finish_reason": response.finish_reason,
                "timestamp": time.time(),
            })

        # Update running totals
        self._total_cost += response.cost_usd
        self._total_prompt_tokens += response.prompt_tokens
        self._total_completion_tokens += response.completion_tokens

        return response

    def _call_api(
        self,
        model: str,
        messages: list[Message],
        params: dict[str, Any],
    ) -> LLMResponse:
        """Make the actual OpenRouter API call."""
        if not self.api_key:
            msg = (
                "No API key configured. Set OPENROUTER_API_KEY environment variable "
                "or pass api_key to LLMClient."
            )
            raise ValueError(msg)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/bravimpurohit/self-healing-agent",
            "X-Title": "Self-Healing Code Agent",
        }

        body: dict[str, Any] = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            **params,
        }

        start = time.monotonic()

        with httpx.Client(timeout=120.0) as client:
            resp = client.post(
                f"{OPENROUTER_BASE}/chat/completions",
                headers=headers,
                json=body,
            )

        latency = time.monotonic() - start

        if resp.status_code != 200:
            logger.error("OpenRouter API error %d: %s", resp.status_code, resp.text[:500])
            msg = f"OpenRouter API error {resp.status_code}: {resp.text[:200]}"
            raise RuntimeError(msg)

        data = resp.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})

        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)

        # Cost from response or computed
        cost = _compute_cost(model, prompt_tokens, completion_tokens)

        return LLMResponse(
            content=choice["message"]["content"],
            model=data.get("model", model),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
            latency_s=latency,
            cached=False,
            finish_reason=choice.get("finish_reason", ""),
            raw_response=data,
        )

    def estimate_sweep_cost(
        self,
        models: list[str],
        num_tasks: int,
        avg_prompt_tokens: int = 2000,
        avg_completion_tokens: int = 1500,
        max_attempts: int = 5,
        seeds: int = 3,
    ) -> dict[str, Any]:
        """Estimate the cost of a full sweep before running it.

        Returns a breakdown by model and total estimated cost.
        """
        breakdown: dict[str, float] = {}
        total = 0.0

        for model in models:
            # Each task: 1 initial + up to (max_attempts-1) repairs, times seeds
            calls_per_task = max_attempts * seeds
            total_calls = num_tasks * calls_per_task
            cost = _compute_cost(model, avg_prompt_tokens, avg_completion_tokens)
            model_total = cost * total_calls
            breakdown[model] = model_total
            total += model_total

        return {
            "breakdown_by_model": breakdown,
            "total_estimated_usd": total,
            "assumptions": {
                "num_tasks": num_tasks,
                "avg_prompt_tokens": avg_prompt_tokens,
                "avg_completion_tokens": avg_completion_tokens,
                "max_attempts_per_task": max_attempts,
                "seeds": seeds,
            },
        }
