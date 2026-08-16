"""OpenTelemetry instrumentation for the self-healing agent.

Provides spans for the key operations:
  - generate: LLM code generation call
  - sandbox_create: container creation and file copy
  - sandbox_exec: command execution in sandbox
  - parse_failure: traceback parsing
  - grade: test execution and scoring
  - repair: full repair loop iteration
  - run: top-level benchmark run

Exported via OTLP to a configurable collector endpoint.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Generator

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Lazy initialization flag
_initialized = False
_tracer: trace.Tracer | None = None

SERVICE_NAME = "self-healing-agent"
SERVICE_VERSION = "0.1.0"


def init_telemetry(
    endpoint: str | None = None,
    enabled: bool = True,
) -> trace.Tracer:
    """Initialize OpenTelemetry tracing.

    Args:
        endpoint: OTLP collector endpoint (default from env or localhost:4317)
        enabled: whether to actually export spans (can disable for tests)

    Returns:
        configured tracer instance
    """
    global _initialized, _tracer

    if _initialized and _tracer is not None:
        return _tracer

    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "service.version": SERVICE_VERSION,
    })

    provider = TracerProvider(resource=resource)

    if enabled:
        if endpoint is None:
            endpoint = os.environ.get(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "http://localhost:4317",
            )

        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                OTLPSpanExporter,
            )

            exporter = OTLPSpanExporter(endpoint=endpoint)
            provider.add_span_processor(BatchSpanProcessor(exporter))
        except Exception:
            # If OTLP exporter fails (no collector running), that's fine
            pass

    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer(SERVICE_NAME, SERVICE_VERSION)
    _initialized = True
    return _tracer


def get_tracer() -> trace.Tracer:
    """Get the configured tracer, initializing if needed."""
    global _tracer
    if _tracer is None:
        return init_telemetry(enabled=bool(os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")))
    return _tracer


@contextmanager
def span(
    name: str,
    attributes: dict[str, Any] | None = None,
) -> Generator[trace.Span, None, None]:
    """Create a traced span with optional attributes.

    Usage:
        with span("generate", {"model": "gpt-4o", "task": "fizzbuzz"}) as s:
            result = call_llm(...)
            s.set_attribute("tokens", result.total_tokens)
    """
    tracer = get_tracer()
    with tracer.start_as_current_span(name) as s:
        if attributes:
            for key, value in attributes.items():
                if isinstance(value, (str, int, float, bool)):
                    s.set_attribute(key, value)
        yield s


@contextmanager
def span_generate(model: str, task_id: str) -> Generator[trace.Span, None, None]:
    """Span for LLM generation calls."""
    with span("generate", {"llm.model": model, "task.id": task_id}) as s:
        yield s


@contextmanager
def span_sandbox_create(task_id: str, attempt: int) -> Generator[trace.Span, None, None]:
    """Span for sandbox container creation."""
    with span("sandbox_create", {"task.id": task_id, "attempt": attempt}) as s:
        yield s


@contextmanager
def span_sandbox_exec(task_id: str, command: str) -> Generator[trace.Span, None, None]:
    """Span for command execution in sandbox."""
    with span("sandbox_exec", {"task.id": task_id, "command": command}) as s:
        yield s


@contextmanager
def span_parse_failure(task_id: str) -> Generator[trace.Span, None, None]:
    """Span for traceback parsing."""
    with span("parse_failure", {"task.id": task_id}) as s:
        yield s


@contextmanager
def span_grade(task_id: str, test_type: str) -> Generator[trace.Span, None, None]:
    """Span for test grading (visible or hidden)."""
    with span("grade", {"task.id": task_id, "test_type": test_type}) as s:
        yield s


@contextmanager
def span_repair(task_id: str, attempt: int) -> Generator[trace.Span, None, None]:
    """Span for a single repair loop iteration."""
    with span("repair", {"task.id": task_id, "attempt": attempt}) as s:
        yield s


@contextmanager
def span_run(run_id: str, model: str, seed: int) -> Generator[trace.Span, None, None]:
    """Span for a full benchmark run."""
    with span("run", {"run.id": run_id, "llm.model": model, "run.seed": seed}) as s:
        yield s
