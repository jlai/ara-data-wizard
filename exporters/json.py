import json
import types
from littletable import Table
from game_data.database import GameDatabase


def serialize(obj):
    if isinstance(obj, types.SimpleNamespace):
        return vars(obj)
    return obj


def organize_by_id(table: Table):
    return dict((entry.id, entry) for entry in table)


def generate_json(output_filename: str, db: GameDatabase):
    tables = {
        "improvements": organize_by_id(db.improvements),
        "techs": organize_by_id(db.techs),
        "buffs": organize_by_id(db.buffs),
        "eras": organize_by_id(db.eras),
    }

    with open(output_filename, "w") as f:
        json.dump(tables, f, indent=4, default=serialize)
