import pytest
from solution import Schema, Migrator


def test_type_coercion_int_to_str():
    v1 = Schema("data", 1)
    v1.add_field("code", "int")

    v2 = Schema("data", 2)
    v2.add_field("code", "str")

    migrator = Migrator(v1, v2)
    result = migrator.migrate({"code": 42})
    assert result == {"code": "42"}
    assert v2.validate(result) is True


def test_type_coercion_str_to_int():
    v1 = Schema("data", 1)
    v1.add_field("count", "str")

    v2 = Schema("data", 2)
    v2.add_field("count", "int")

    migrator = Migrator(v1, v2)
    result = migrator.migrate({"count": "7"})
    assert result == {"count": 7}


def test_type_coercion_float_to_int():
    v1 = Schema("data", 1)
    v1.add_field("value", "float")

    v2 = Schema("data", 2)
    v2.add_field("value", "int")

    migrator = Migrator(v1, v2)
    result = migrator.migrate({"value": 3.9})
    assert result == {"value": 3}


def test_type_coercion_bool_to_int():
    v1 = Schema("data", 1)
    v1.add_field("flag", "bool")

    v2 = Schema("data", 2)
    v2.add_field("flag", "int")

    migrator = Migrator(v1, v2)
    assert migrator.migrate({"flag": True}) == {"flag": 1}
    assert migrator.migrate({"flag": False}) == {"flag": 0}


def test_migrate_batch():
    v1 = Schema("user", 1)
    v1.add_field("name", "str")

    v2 = Schema("user", 2)
    v2.add_field("name", "str")
    v2.add_field("active", "bool", default=True)

    migrator = Migrator(v1, v2)
    records = [{"name": "A"}, {"name": "B"}]
    results = migrator.migrate_batch(records)
    assert results == [
        {"name": "A", "active": True},
        {"name": "B", "active": True},
    ]


def test_validate_bool_not_confused_with_int():
    s = Schema("data", 1)
    s.add_field("count", "int")
    assert s.validate({"count": True}) is False


def test_validate_missing_required_field():
    s = Schema("data", 1)
    s.add_field("name", "str")
    s.add_field("age", "int")
    assert s.validate({"name": "x"}) is False


def test_migrated_record_validates_against_target():
    v1 = Schema("prod", 1)
    v1.add_field("name", "str")
    v1.add_field("price", "int")

    v2 = Schema("prod", 2)
    v2.add_field("name", "str")
    v2.add_field("price", "float")
    v2.add_field("in_stock", "bool", default=True)

    migrator = Migrator(v1, v2)
    result = migrator.migrate({"name": "Widget", "price": 10})
    assert v2.validate(result) is True
    assert result == {"name": "Widget", "price": 10.0, "in_stock": True}
