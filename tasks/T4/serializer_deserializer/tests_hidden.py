from solution import serialize, deserialize


def test_deeply_nested():
    obj = {"a": {"b": {"c": {"d": [1, 2, 3]}}}}
    assert deserialize(serialize(obj)) == obj


def test_special_characters_in_strings():
    obj = {"key:with:colons": "value[with]brackets,and,commas"}
    assert deserialize(serialize(obj)) == obj


def test_mixed_list():
    obj = [1, "two", 3.0, None, True, False, {"nested": "dict"}]
    assert deserialize(serialize(obj)) == obj


def test_int_vs_float_preserved():
    obj = {"int_val": 1, "float_val": 1.0}
    result = deserialize(serialize(obj))
    assert result["int_val"] == 1 and isinstance(result["int_val"], int)
    assert result["float_val"] == 1.0 and isinstance(result["float_val"], float)


def test_empty_string():
    obj = {"empty": "", "nested": ["", ""]}
    assert deserialize(serialize(obj)) == obj


def test_large_numbers():
    obj = {"big": 99999999999999, "neg": -42, "float": -3.14159}
    assert deserialize(serialize(obj)) == obj


def test_boolean_not_confused_with_string():
    obj = {"flag": True, "text": "True"}
    result = deserialize(serialize(obj))
    assert result["flag"] is True
    assert result["text"] == "True" and isinstance(result["text"], str)


def test_list_of_dicts():
    obj = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
    assert deserialize(serialize(obj)) == obj
