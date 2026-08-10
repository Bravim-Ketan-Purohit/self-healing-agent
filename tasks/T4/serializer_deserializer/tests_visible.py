from solution import serialize, deserialize


def test_roundtrip_simple_dict():
    obj = {"name": "alice", "age": 30}
    assert deserialize(serialize(obj)) == obj


def test_roundtrip_nested():
    obj = {"a": [1, 2, {"b": True}], "c": None}
    assert deserialize(serialize(obj)) == obj


def test_roundtrip_empty_containers():
    assert deserialize(serialize({})) == {}
    assert deserialize(serialize([])) == []


def test_roundtrip_primitives():
    for val in [42, 3.14, True, False, None, "hello"]:
        assert deserialize(serialize(val)) == val
