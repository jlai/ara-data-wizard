import types


def ensure_dict(obj):
    if isinstance(obj, types.SimpleNamespace):
        return vars(obj)
    elif isinstance(obj, list):
        return dict([(x, 1) for x in obj])
    elif obj is None:
        return {}
    return obj


def has_flag(obj, flag, flag_key="Flags"):
    flags = getattr(obj, flag_key, []) or []
    return flag in flags
