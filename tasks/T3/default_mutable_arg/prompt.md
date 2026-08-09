# Default Mutable Argument

Implement a `Logger` class with a `log(msg: str, tags: list[str] | None = None) -> dict` method.

Each call to `log` creates a log entry (dict) with the message and its tags. If `tags` is not provided, the entry should have an empty list of tags.

The `Logger.log` method returns the log entry: `{"msg": msg, "tags": tags}`.

Tags provided to one call should never appear in other log entries. Each log entry's tags list is independent.

## Examples

```python
logger = Logger()
entry1 = logger.log("hello")
# {"msg": "hello", "tags": []}

entry2 = logger.log("world", tags=["info"])
# {"msg": "world", "tags": ["info"]}

entry3 = logger.log("test")
# {"msg": "test", "tags": []}
# entry3["tags"] is NOT the same list object as entry1["tags"]
```

## Constraints

- Each log entry is independent — mutating one entry's tags must not affect others.
- The class should store all entries in a `self.entries` list attribute.
- `log` returns the entry dict it just created.
