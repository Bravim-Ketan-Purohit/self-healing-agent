from solution import transform


def test_basic_transform():
    data = {"a": 1, "b": 2}
    result = transform(data, "a", lambda x: x * 10)
    assert result == {"a": 10, "b": 2}


def test_nested_transform():
    data = {"a": 1, "b": {"a": 2, "c": 3}}
    result = transform(data, "a", lambda x: x * 10)
    assert result == {"a": 10, "b": {"a": 20, "c": 3}}


def test_no_matching_key():
    data = {"x": 1, "y": 2}
    result = transform(data, "z", lambda x: x * 10)
    assert result == {"x": 1, "y": 2}
