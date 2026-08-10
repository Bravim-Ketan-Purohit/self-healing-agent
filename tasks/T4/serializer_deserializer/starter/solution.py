"""
Custom serializer/deserializer.

Implement serialize() and deserialize() such that deserialize(serialize(x)) == x
for nested dicts, lists, strings, ints, floats, booleans, and None.

Do NOT use json, pickle, ast.literal_eval, or any built-in serialization library.
"""


def serialize(obj):
    """Serialize a Python object to a custom string format."""
    raise NotImplementedError


def deserialize(s):
    """Deserialize a custom string format back to a Python object."""
    raise NotImplementedError
