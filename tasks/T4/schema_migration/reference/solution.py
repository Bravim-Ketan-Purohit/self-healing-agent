"""Schema and Migrator that agree on field types and migration rules."""


_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}


def _coerce(value, source_type, target_type):
    """Coerce a value from source_type to target_type."""
    if source_type == target_type:
        return value
    target_cls = _TYPE_MAP[target_type]
    return target_cls(value)


class Schema:
    """Defines the structure of a data record."""

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self._fields = {}

    def add_field(self, name, field_type, default=None):
        """Add a field to the schema.

        field_type: one of 'str', 'int', 'float', 'bool'
        default: default value for the field (None means required)
        """
        if field_type not in _TYPE_MAP:
            raise ValueError(f"Unsupported type: {field_type}")
        self._fields[name] = {"type": field_type, "default": default}

    def validate(self, record):
        """Return True if record matches this schema."""
        for field_name, field_info in self._fields.items():
            if field_name not in record:
                if field_info["default"] is None:
                    return False
                continue
            value = record[field_name]
            expected_type = _TYPE_MAP[field_info["type"]]
            # bool is subclass of int, so check bool first
            if field_info["type"] == "int" and isinstance(value, bool):
                return False
            if field_info["type"] == "float" and isinstance(value, bool):
                return False
            if field_info["type"] == "bool":
                if not isinstance(value, bool):
                    return False
            elif not isinstance(value, expected_type):
                # Allow int where float is expected
                if field_info["type"] == "float" and isinstance(value, int):
                    continue
                return False
        return True

    def get_fields(self):
        """Return dict of {field_name: {'type': type_str, 'default': default}}."""
        return dict(self._fields)


class Migrator:
    """Transforms records from source schema to target schema."""

    def __init__(self, source_schema, target_schema):
        self.source_schema = source_schema
        self.target_schema = target_schema

    def migrate(self, record):
        """Transform a record from source schema to target schema.

        - Fields in target but not source: use target's default.
        - Fields in source but not target: drop them.
        - Fields in both: keep value, coerce type if needed.
        """
        source_fields = self.source_schema.get_fields()
        target_fields = self.target_schema.get_fields()
        result = {}

        for field_name, field_info in target_fields.items():
            if field_name in record:
                source_type = source_fields.get(field_name, {}).get("type")
                target_type = field_info["type"]
                if source_type and source_type != target_type:
                    result[field_name] = _coerce(record[field_name], source_type, target_type)
                else:
                    result[field_name] = record[field_name]
            else:
                result[field_name] = field_info["default"]

        return result

    def migrate_batch(self, records):
        """Migrate a list of records."""
        return [self.migrate(r) for r in records]
