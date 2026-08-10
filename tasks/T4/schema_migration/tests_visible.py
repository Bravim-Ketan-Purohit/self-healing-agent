from solution import Schema, Migrator


def test_migrate_adds_new_field_with_default():
    v1 = Schema("user", 1)
    v1.add_field("name", "str")

    v2 = Schema("user", 2)
    v2.add_field("name", "str")
    v2.add_field("age", "int", default=0)

    migrator = Migrator(v1, v2)
    result = migrator.migrate({"name": "Alice"})
    assert result == {"name": "Alice", "age": 0}


def test_migrate_drops_removed_field():
    v1 = Schema("user", 1)
    v1.add_field("name", "str")
    v1.add_field("temp", "str")

    v2 = Schema("user", 2)
    v2.add_field("name", "str")

    migrator = Migrator(v1, v2)
    result = migrator.migrate({"name": "Bob", "temp": "x"})
    assert result == {"name": "Bob"}


def test_validate_correct_record():
    s = Schema("item", 1)
    s.add_field("id", "int")
    s.add_field("name", "str")
    assert s.validate({"id": 1, "name": "widget"}) is True


def test_validate_wrong_type():
    s = Schema("item", 1)
    s.add_field("id", "int")
    assert s.validate({"id": "not_int"}) is False
