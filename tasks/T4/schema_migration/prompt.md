# Schema & Migrator

## Problem

Implement two classes that work together to define data schemas and migrate records between schema versions:

1. **`Schema`** - Defines the structure of a data record:
   - `__init__(self, name, version)` - Creates a schema with a name and version number.
   - `add_field(name, field_type, default=None)` - Adds a field with a type and optional default.
   - `validate(record)` - Returns True if the record dict matches the schema (all required fields present with correct types).
   - `get_fields()` - Returns a dict of `{field_name: {"type": field_type, "default": default}}`.

2. **`Migrator`** - Transforms data records from one schema version to another:
   - `__init__(self, source_schema, target_schema)` - Takes source and target Schema objects.
   - `migrate(record)` - Transform a record from source schema to target schema:
     - Fields in target but not source: fill with the target field's default value.
     - Fields in source but not target: drop them.
     - Fields in both: keep the value (with type coercion if types differ).
   - `migrate_batch(records)` - Migrate a list of records.

## Supported Field Types

- `"str"` - string
- `"int"` - integer
- `"float"` - float
- `"bool"` - boolean

## Type Coercion Rules (when field exists in both schemas but type changed)

- int -> str: `str(value)`
- str -> int: `int(value)` (raise ValueError if not convertible)
- int -> float: `float(value)`
- float -> int: `int(value)` (truncate)
- bool -> int: 1 or 0
- int -> bool: `bool(value)`

## Interface Contract

- Migrator uses `Schema.get_fields()` to determine what fields exist and their types/defaults.
- `Schema.validate(record)` returns True for records that match the schema.
- After `Migrator.migrate(record)`, the result must pass `target_schema.validate(result)`.

## Constraints

- Both classes must be in the same `solution.py` file.
