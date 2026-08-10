"""
Custom serializer/deserializer using a length-prefixed format.
Format: TYPE:LENGTH:DATA
Types: D=dict, L=list, S=string, I=int, F=float, B=bool, N=none
"""


def serialize(obj):
    """Serialize a Python object to a custom string format."""
    if obj is None:
        return "N:0:"
    elif isinstance(obj, bool):
        val = "1" if obj else "0"
        return f"B:{len(val)}:{val}"
    elif isinstance(obj, int):
        val = str(obj)
        return f"I:{len(val)}:{val}"
    elif isinstance(obj, float):
        val = repr(obj)
        return f"F:{len(val)}:{val}"
    elif isinstance(obj, str):
        return f"S:{len(obj)}:{obj}"
    elif isinstance(obj, list):
        parts = []
        for item in obj:
            parts.append(serialize(item))
        joined = "".join(parts)
        return f"L:{len(joined)}:{joined}"
    elif isinstance(obj, dict):
        parts = []
        for key, value in obj.items():
            parts.append(serialize(key))
            parts.append(serialize(value))
        joined = "".join(parts)
        return f"D:{len(joined)}:{joined}"
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")


def deserialize(s):
    """Deserialize a custom string format back to a Python object."""
    obj, _ = _deserialize_at(s, 0)
    return obj


def _deserialize_at(s, pos):
    """Deserialize starting at position pos, return (obj, new_pos)."""
    type_char = s[pos]
    pos += 1  # skip type char
    assert s[pos] == ":"
    pos += 1  # skip first colon

    # Read length
    colon_pos = s.index(":", pos)
    length = int(s[pos:colon_pos])
    pos = colon_pos + 1  # skip second colon

    data = s[pos:pos + length]
    new_pos = pos + length

    if type_char == "N":
        return None, new_pos
    elif type_char == "B":
        return data == "1", new_pos
    elif type_char == "I":
        return int(data), new_pos
    elif type_char == "F":
        return float(data), new_pos
    elif type_char == "S":
        return data, new_pos
    elif type_char == "L":
        items = []
        inner_pos = pos
        while inner_pos < pos + length:
            item, inner_pos = _deserialize_at(s, inner_pos)
            items.append(item)
        return items, new_pos
    elif type_char == "D":
        d = {}
        inner_pos = pos
        while inner_pos < pos + length:
            key, inner_pos = _deserialize_at(s, inner_pos)
            value, inner_pos = _deserialize_at(s, inner_pos)
            d[key] = value
        return d, new_pos
    else:
        raise ValueError(f"Unknown type: {type_char}")
