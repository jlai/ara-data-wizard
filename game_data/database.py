from itertools import chain
import os
import glob
from pathlib import PurePath
import types
from warnings import warn
from littletable import Table
from .eras import ERA_RANKS

from game_data.translations import (
    LocalizedLine,
    LocalizedStrings,
    parse_translation_file,
)

from .zdata.parse import parse_zdata_file


def ensure_dict(obj):
    if isinstance(obj, types.SimpleNamespace):
        return vars(obj)
    elif isinstance(obj, list):
        return dict([(x, 1) for x in obj])
    elif obj is None:
        return {}
    return obj


def get_tech_unlocks_ids(tech):
    return (
        getattr(tech, "UnlockImprovementsIDs", [])
        + getattr(tech, "UnlockRecipesIDs", [])
        + getattr(tech, "UnlockFormationsIDs", [])
        + getattr(tech, "UnlockGovernmentsIDs", [])
        + getattr(tech, "UnlockCitySpecialProjects", [])
        + getattr(tech, "UnlockCityMissileProjects", [])
        + [obj["Value"] for obj in getattr(tech, "UnlockNaturalResourcesIDs", [])]
    )


def get_tech_obsoletes_ids(tech):
    return (
        getattr(tech, "ObsoleteImprovementIDs", [])
        + getattr(tech, "ObsoleteCityUnitProjectIDs", [])
        + getattr(tech, "ObsoleteRecipes", [])
    )


def glob_assets(assets_dir, include, exclude="*DLC*"):
    matches = glob.glob(include, root_dir=assets_dir)

    return [path for path in matches if not PurePath(path).match(exclude)]


class GameDatabase:
    def __init__(self, assets_dir):
        if not os.path.exists(assets_dir):
            raise Exception(f"assets directory {assets_dir} does not exist")

        self.assets_dir = assets_dir

        self.eras = Table("eras")
        self.eras.create_index("id", unique=True)
        self.unlocks = Table("unlocks")
        self.unlocks.create_index("unlocks_id")
        self.supplies = Table("supplies")
        self.supplies.create_index("item_id")
        self.construction_costs = Table("construction_costs")
        self.construction_costs.create_index("item_id")

        self.translations = self.load_translations()
        self.rules = self.load_game_rules()

        self.improvements = self.load_table("improvements", "Improvements*.zdata")
        self.techs = self.load_table("techs", "Technologies*.zdata")
        self.items = self.load_table("items", "Items*.zdata")
        self.buffs = self.load_table("buffs", "Buffs/Buffs*.zdata")
        self.recipes = self.load_table("recipes", "Recipes*.zdata")
        self.units = self.load_table("units", "Units*.zdata")
        self.formations = self.load_table("formations", "ArmyTemplates*.zdata")
        self.governments = self.load_table("governments", "Governments*.zdata")
        self.city_unit_projects = self.load_table(
            "city_unit_projects", "CityUnitProjects*.zdata"
        )
        self.city_special_projects = self.load_table(
            "city_special_projects", "CitySpecialProjects*.zdata"
        )
        self.city_missile_projects = self.load_table(
            "city_missile_projects", "CityMissileProjects*.zdata"
        )

        self.build_crossrefs()

    def load_table(self, name, glob_pattern):
        table = Table(name)
        table.create_index("id", unique=True)
        return self.load_into_table(table, glob_pattern)

    def get_text(self, key, *, count=1, params={}, quiet=False):
        line = self.translations.lines.get(key)

        if not line:
            if not quiet:
                warn(f"could not find text {key}")
            return f"[MISSING TEXT: {key}]"

        return self.translations.interpolate(line, count=count, params=params)

    def get_item_quantities(self, d: dict | types.SimpleNamespace | list):
        texts = []

        if isinstance(d, types.SimpleNamespace):
            d = vars(d)
        elif isinstance(d, list):
            d = dict([(x, 1) for x in d])

        for key, count in d.items():
            item = self.items.by.id[key]
            item_name = self.get_text(item.Name, count=count)
            texts.append(f"{count:d} {item_name}")

        return texts

    def build_crossrefs(self):
        for tech in self.techs:
            for unlock in get_tech_unlocks_ids(tech):
                self.unlocks.insert(
                    {
                        "unlocks_id": unlock,
                        "tech_id": tech.id,
                        "era_id": tech.Era,
                        "era_rank": ERA_RANKS[tech.Era],
                    }
                )

        for improvement in self.improvements:
            for item_id in set(
                chain.from_iterable(
                    slot["Options"].keys() for slot in improvement.ItemOptions
                )
            ):
                self.supplies.insert(
                    {
                        "item_id": item_id,
                        "improvement_id": improvement.id,
                        "improvement_name": improvement.Name,
                    }
                )

            for item_id, count in ensure_dict(
                improvement.BuildImprovementItemCost
            ).items():
                self.construction_costs.insert(
                    {
                        "construction_name": improvement.Name,
                        "item_id": item_id,
                        "count_needed": count,
                    }
                )

        for project in self.city_unit_projects:
            unit_item = self.items.by.id[project.UnitItemCreated]

            for item_id, count in ensure_dict(project.ItemCost).items():
                self.construction_costs.insert(
                    {
                        "construction_name": unit_item.Name,
                        "item_id": item_id,
                        "count_needed": count,
                    }
                )

    def load_translations(self, locale_id="en"):
        lines: dict[str, LocalizedLine] = {}

        for path in glob.glob(f"Text/{locale_id}/*.xml", root_dir=self.assets_dir):
            locale_data = parse_translation_file(os.path.join(self.assets_dir, path))
            lines.update(locale_data.lines)

        return LocalizedStrings(locale_id, lines)

    def load_zdata_files(self, glob_path: str):
        zdata_path = os.path.join(self.assets_dir, "SourceMods")

        for path in glob_assets(zdata_path, glob_path):
            yield parse_zdata_file(os.path.join(zdata_path, path))

    def load_into_table(self, table: Table, glob_path: str):
        for zdata in self.load_zdata_files(glob_path):
            for id, data in zdata.exports.items():
                try:
                    table.insert({"id": id, **data})
                except Exception as e:
                    raise Exception(f"error inserting {id} into local table") from e

        return table

    def load_game_rules(self):
        rules = {}

        for zdata in self.load_zdata_files("GameRules/*.zdata"):
            root = zdata.exports.get("Root")

            if root and "_type" in root:
                rules[root["_type"]] = root

        base_game_rules = rules["BaseGameRulesDef"]

        for id, data in base_game_rules["TechEraData"].items():
            if id != "RulesTypes.TechEras.NumTechEras":
                self.eras.insert({"id": id, **data})

        return rules

    def get_earliest_era_id(self, unlock_id: str):
        earliest_unlock = min(
            self.unlocks.by.unlocks_id[unlock_id],
            default=None,
            key=lambda u: u.era_rank,
        )
        if earliest_unlock:
            return earliest_unlock.era_id
        return ""

    def get_recipe_product(self, recipe_id):
        "Resolve recipe to a normal item or a unit (instead of the pseudo-item for a unit)"
        recipe = self.recipes.by.id[recipe_id]
        item = self.items.by.id[recipe.ItemCreated]

        if getattr(item, "TargetUnitID", None):
            unit = self.units.by.id[item.TargetUnitID]
            return (item.TargetUnitID, unit.Name)

        return (item.id, item.Name)

    def get_name_text(self, id: str):
        return self.get_text(self.get_name_key(id))

    def get_name_key(self, id: str):
        prefix = id.split("_", 1)[0]

        match prefix:
            case "imp":
                return self.improvements.by.id[id].Name
            case "itm":
                return self.items.by.id[id].Name
            case "rcp":
                return self.get_recipe_product(id)[1]
            case "tch":
                return self.techs.by.id[id].Name
            case "unt":
                return self.units.by.id[id].Name
            case "frm":
                return self.formations.by.id[id].Name
            case "gvt":
                return self.governments.by.id[id].m_Name
            case "cup":
                cup = self.city_unit_projects.by.id[id]
                item = self.items.by.id[cup.UnitItemCreated]
                unit = self.units.by.id[item.TargetUnitID]
                return unit.Name
            case "csp":
                return self.city_special_projects.by.id[id].Name
            case "cmp":
                return self.city_missile_projects.by.id[id].Name
