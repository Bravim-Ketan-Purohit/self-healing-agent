"""Schema and Migrator.

Schema defines fields with types and defaults.
Migrator transforms records from one schema version to another.
"""


class Schema:
    """Defines the structure of a data record."""

    def __init__(self, name, version):
        raise NotImplementedError

    def add_field(self, name, field_type, default=None):
        """Add a field. field_type: 'str', 'int', 'float', or 'bool'."""
        raise NotImplementedError

    def validate(self, record):
        """Return True if record matches this schema."""
        raise NotImplementedError

    def get_fields(self):
        """Return {field_name: {'type': type_str, 'default': default}}."""
        raise NotImplementedError


class Migrator:
    """Transforms records from source schema to target schema."""

    def __init__(self, source_schema, target_schema):
        raise NotImplementedError

    def migrate(self, record):
        """Transform record: add new fields with defaults, drop removed, coerce types."""
        raise NotImplementedError

    def migrate_batch(self, records):
        """Migrate a list of records."""
        raise NotImplementedError
