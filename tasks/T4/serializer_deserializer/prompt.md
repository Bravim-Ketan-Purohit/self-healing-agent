# Serializer & Deserializer

## Problem

Implement two functions that must be exact inverses of each other:

1. **`serialize(obj)`** - Converts a Python object (nested dicts, lists, strings, ints, floats, booleans, and None) into a custom string format.

2. **`deserialize(s)`** - Converts the custom string format back into the original Python object.

## Interface Contract

- `deserialize(serialize(x)) == x` must hold for all valid inputs.
- The serialization format is up to you, but it must handle:
  - Nested dictionaries
  - Nested lists
  - Strings (including those with special characters like colons, brackets, commas)
  - Integers and floats (must preserve type: `serialize(1)` vs `serialize(1.0)`)
  - Booleans (`True`/`False` must not be confused with strings)
  - `None`
- Empty containers: `{}` and `[]` must roundtrip correctly.
- Dict keys are always strings.

## Constraints

- Do NOT use `json`, `pickle`, `ast.literal_eval`, or any built-in serialization library.
- You must invent your own format and parsing logic.
- Both functions must be in the same `solution.py` file.
