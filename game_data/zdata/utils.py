import types


def ensure_dict(obj):
    if isinstance(obj, types.SimpleNamespace):
        return vars(obj)
    elif isinstance(obj, list):
        return dict([(x, 1) for x in obj])
    elif obj is None:
        return {}
    return obj
