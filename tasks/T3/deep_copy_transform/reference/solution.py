import copy


def transform(data: dict, key: str, func: callable) -> dict:
    """Apply func to all values at 'key' in nested dicts, returning a new dict."""
    result = {}
    for k, v in data.items():
        if k == key:
            if isinstance(v, dict):
                # Apply func to the value, but also recurse into it
                result[k] = func(_recurse(v, key, func))
            else:
                result[k] = func(v)
        elif isinstance(v, dict):
            result[k] = _recurse(v, key, func)
        else:
            result[k] = copy.deepcopy(v)
    return result


def _recurse(data: dict, key: str, func: callable) -> dict:
    """Recursively transform nested dicts."""
    result = {}
    for k, v in data.items():
        if k == key:
            if isinstance(v, dict):
                result[k] = func(_recurse(v, key, func))
            else:
                result[k] = func(v)
        elif isinstance(v, dict):
            result[k] = _recurse(v, key, func)
        else:
            result[k] = copy.deepcopy(v)
    return result
