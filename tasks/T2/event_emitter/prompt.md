# Event Emitter

Implement an `EventEmitter` class that provides a publish/subscribe event system:

- `on(event: str, callback: Callable) -> None` — Register a callback for an event. The same callback can be registered multiple times.
- `off(event: str, callback: Callable) -> None` — Remove one registration of a callback for an event. If the callback is not registered, do nothing (no error).
- `once(event: str, callback: Callable) -> None` — Register a callback that fires at most once, then auto-removes itself.
- `emit(event: str, *args, **kwargs) -> None` — Call all registered callbacks for the event with the given arguments. Callbacks are called in registration order. If no callbacks are registered, do nothing.

## Invariants

- Callbacks are called in the order they were registered.
- A `once` listener fires exactly once, even if `emit` is called multiple times.
- Removing a callback during `emit` does not affect the current emission (all callbacks registered at the time emit was called will fire).
- `off` removes only one registration if a callback was added multiple times.

## Examples

```python
ee = EventEmitter()
results = []
ee.on("data", lambda x: results.append(x))
ee.emit("data", 42)
results  # [42]
ee.emit("data", 99)
results  # [42, 99]
```
