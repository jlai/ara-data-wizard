from dataclasses import dataclass, field
import json
import types
from game_data.database import GameDatabase
from game_data.zdata.utils import ensure_dict


def organize_by_id(objects):
    return dict((entry["id"], entry) for entry in objects)


@dataclass(kw_only=True)
class JsonFilter:
    type: str | list[str] = None
    exclude: bool = False
    remove_properties: list[str] = field(default_factory=list)

    @staticmethod
    def from_json(json_obj):
        return JsonFilter(
            type=json_obj.get("type", None),
            exclude=json_obj.get("exclude", False),
            remove_properties=json_obj.get("remove-properties", False),
        )

    def update_object(self, obj):
        obj = ensure_dict(obj)

        if not match_filter_property(obj.get("_type", None), self.type):
            return obj

        if self.remove_properties:
            obj = dict(
                (key, value)
                for (key, value) in obj.items()
                if key not in self.remove_properties
            )

        if self.exclude:
            return None

        return obj


@dataclass(kw_only=True)
class ExportJsonOptions:
    groups: list[str] = field(default_factory=list)
    translate_text: bool = False
    normalize_case: bool = True
    filters: list[JsonFilter] = field(default_factory=list)


def match_filter_property(value, rule_value):
    if not value:
        return False

    if not rule_value:
        return True

    if isinstance(rule_value, list):
        return value in rule_value
    else:
        return value == rule_value


def make_serialize(options, db=None):
    def serialize(obj):
        if isinstance(obj, types.SimpleNamespace):
            obj = vars(obj)

        if isinstance(obj, str) and obj.startswith("TXT_") and options.translate_text:
            obj = db.get_text(obj, quiet=True)

        if isinstance(obj, dict):
            if options.normalize_case:
                obj = dict(
                    (
                        (f"{key[0].lower()}{key[1:]}", value)
                        if "." not in key
                        else (key, value)
                    )
                    for (key, value) in obj.items()
                )

        return obj

    return serialize


def match_filter_property(value, rule_value):
    if not value:
        return False

    if not rule_value:
        return True

    if isinstance(rule_value, list):
        return value in rule_value
    else:
        return value == rule_value


def generate_json(output_filename: str, db: GameDatabase, options=ExportJsonOptions()):
    filtered_game_data = {}
    for group_name, entries in db.game_data.items():

        if options.groups and group_name not in options.groups:
            continue

        filtered_entries = {}
        for key, entry in entries.items():
            updated_obj = entry

            for obj_filter in options.filters:
                updated_obj = obj_filter.update_object(updated_obj)
                if not updated_obj:
                    break
            if updated_obj:
                filtered_entries[key] = updated_obj
        filtered_game_data[group_name] = filtered_entries

    with open(output_filename, "w") as f:
        json.dump(
            transform(filtered_game_data, pre_func=make_serialize(options, db=db)),
            f,
            indent=4,
        )


identity = lambda x: x


def transform(obj, *, pre_func=identity, post_func=identity, memo=None):
    "Recursively clone and transform object"

    if memo is None:
        memo = {}

    identity = id(obj)
    if identity in memo:
        return memo[identity]

    obj = pre_func(obj)

    if isinstance(obj, dict):
        obj = dict(
            (key, transform(value, pre_func=pre_func, post_func=post_func, memo=memo))
            for key, value in obj.items()
        )
    elif isinstance(obj, types.SimpleNamespace):
        obj = types.SimpleNamespace(
            dict(
                (
                    key,
                    transform(value, pre_func=pre_func, post_func=post_func, memo=memo),
                )
                for key, value in vars(obj).items()
            )
        )
    elif isinstance(obj, (list, tuple)):
        obj = [
            transform(value, pre_func=pre_func, post_func=post_func, memo=memo)
            for value in obj
        ]

    obj = post_func(obj)

    memo[identity] = obj
    return obj
