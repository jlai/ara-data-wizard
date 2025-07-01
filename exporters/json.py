from dataclasses import dataclass, field
import json
import types
from littletable import Table
from game_data.database import GameDatabase


def organize_by_id(table: Table):
    return dict((entry.id, entry) for entry in table)


@dataclass(kw_only=True)
class ExportJsonOptions:
    translate_text: bool = False
    remove_properties: list[str] = field(default_factory=list)
    normalize_case: bool = False


def make_serialize(options, db=None):
    def serialize(obj):
        if isinstance(obj, types.SimpleNamespace):
            obj = vars(obj)

        if isinstance(obj, str) and obj.startswith("TXT_") and options.translate_text:
            obj = db.get_text(obj, quiet=True)

        if isinstance(obj, dict):
            updates = {}

            if options.remove_properties:
                obj = dict(
                    (key, value)
                    for (key, value) in obj.items()
                    if key not in options.remove_properties
                )

            if options.normalize_case:
                obj = dict(
                    (
                        (f"{key[0].lower()}{key[1:]}", value)
                        if "." not in key
                        else (key, value)
                    )
                    for (key, value) in obj.items()
                )

            if updates:
                obj = obj | updates

        return obj

    return serialize


def generate_json(output_filename: str, db: GameDatabase, options=ExportJsonOptions()):
    tables = {
        "improvements": organize_by_id(db.improvements),
        "techs": organize_by_id(db.techs),
        "items": organize_by_id(db.items),
        "recipes": organize_by_id(db.recipes),
        "units": organize_by_id(db.units),
        "formations": organize_by_id(db.formations),
        "buffs": organize_by_id(db.buffs),
        "governments": organize_by_id(db.governments),
        "citySpecialProjects": organize_by_id(db.city_special_projects),
        "cityUnitProjects": organize_by_id(db.city_unit_projects),
        "cityMissileProjects": organize_by_id(db.city_missile_projects),
        "eras": organize_by_id(db.eras),
    }

    with open(output_filename, "w") as f:
        json.dump(
            transform(tables, pre_func=make_serialize(options, db=db)), f, indent=4
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
