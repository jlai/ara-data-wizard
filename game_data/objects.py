from dataclasses import dataclass
from pprint import pp
from typing import Union
from warnings import warn
import game_data.database
from game_data.zdata.utils import ensure_dict


class GameObject:
    NAME_PROP = "Name"

    def __init__(self, id: str, data: dict, *, db: "game_data.database.GameDatabase"):
        self.id = id
        self.data = data
        self.db = db

    def has_flag(self, flag, flag_key="Flags"):
        flags = self.get(flag_key, []) or []
        return flag in flags

    def get(self, name, default=None):
        return self.data.get(name, default)

    def get_as_dict(self, name):
        return ensure_dict(self.get(name, {}))

    def get_as_list(self, name):
        return self.get(name, [])

    @property
    def name(self):
        return self.data[self.NAME_PROP]

    def get_name(self, **kwargs):
        return self.db.get_text(self.name, **kwargs)


class SimpleGameObject(GameObject):
    def __getattr__(self, name):
        if name not in self.data:
            raise AttributeError(name=name, obj=self.data)

        warn(f"Legacy lookup for {name} in {type(self).__name__}", stacklevel=2)
        return self.data[name]


class Tech(GameObject):
    @property
    def era_id(self):
        return self.data["Era"]

    @property
    def unlocks_ids(self) -> list[str]:
        return (
            self.get("UnlockImprovementsIDs", [])
            + self.get("UnlockRecipesIDs", [])
            + self.get("UnlockFormationIDs", [])
            + self.get("UnlockGovernmentsIDs", [])
            + self.get("UnlockCitySpecialProjects", [])
            + self.get("UnlockCityMissilePorjects", [])
            + [obj["Value"] for obj in self.get("UnlockNaturalResourcesIDs", [])]
        )

    @property
    def obsoletes_ids(self) -> list[str]:
        return (
            self.get("ObsoleteImprovementIDs", [])
            + self.get("ObsoleteCityUnitProjectIDs", [])
            + self.get("ObsoleteRecipes", [])
        )

    @property
    def research_cost(self):
        return self.get("uiResearchCost", None)

    @property
    def is_transition_tech(self):
        return self.has_flag("TechFlags.CapstoneTech")


class Item(SimpleGameObject):
    @property
    def unlocked_by(self):
        return self.db.get_techs_that_unlock(self.id)

    @property
    def target_unit_id(self):
        return self.get("TargetUnitID", None)

    @property
    def is_unit(self):
        return True if self.target_unit_id else False

    @property
    def recipe_id(self):
        return self.get("RecipeID")

    @property
    def recipe(self) -> Union["Recipe", None]:
        if not self.recipe_id:
            return None

        return self.db.recipes.by.id[self.recipe_id]


class Improvement(SimpleGameObject):
    @property
    def unlocked_by(self):
        return self.db.get_techs_that_unlock(self.id)

    @property
    def recipes(self) -> list["Recipe"]:
        return [
            self.db.recipes.by.id[recipe_id] for recipe_id in self.get("Recipes", [])
        ]

    @property
    def production_cost(self):
        return self.get("uiProductionCost")

    @property
    def nation_max_count(self):
        return self.get("uiNationMaxCount")

    @property
    def province_max_count(self):
        return self.get("uiProvinceMaxCount")

    @property
    def is_triumph(self):
        return self.has_flag("GrantedFlag.Triumph", flag_key="GrantedFlags")


class Buff(SimpleGameObject):
    @property
    def modifiers(self):
        return self.get("Modifiers")

    @property
    def description(self):
        return self.get("Description")


class Government(SimpleGameObject):
    NAME_PROP = "m_Name"


class Recipe(SimpleGameObject):
    @property
    def unlocked_by(self):
        return self.db.get_techs_that_unlock(self.id)

    @property
    def ingredients(self):
        return [
            RecipeIngredient(ingredient_data)
            for ingredient_data in self.get("Ingredients")
        ]

    @property
    def product(self):
        item = self.db.items.by.id[self.data["ItemCreated"]]

        target_unit_id = item.get("TargetUnitID")

        if target_unit_id:
            return self.db.units.by.id[target_unit_id]
        else:
            return item

    @property
    def production_cost(self):
        return self.get("ProductionCost")


@dataclass
class RecipeIngredient:
    data: dict

    @property
    def production_bonus(self):
        return self.data["ProductionBonus"]

    @property
    def options(self):
        return self.data["Options"]


class CityUnitProject(SimpleGameObject):
    @property
    def unit_item_id(self):
        return self.get("UnitItemCreated")


class Unit(SimpleGameObject):
    @property
    def item_id(self) -> str:
        return list(self.get_as_dict("ConstructionCost").keys())[0]

    @property
    def item(self) -> "Item":
        return self.db.items.by.id[self.item_id]

    @property
    def recipe(self):
        return self.item.recipe

    @property
    def project(self) -> "CityUnitProject":
        return self.db.city_unit_projects.by.unit_item_id[self.item_id]

    @property
    def base_strength(self):
        return self.get("uiBaseStrength")

    @property
    def base_religion_strength(self):
        return self.get("uiBaseReligionStrength")

    @property
    def base_speed(self):
        return self.get("uiBaseSpeed")

    @property
    def bombard_range(self):
        return self.get("uiBombardRange")

    @property
    def type(self):
        return self.get("Type")

    @property
    def role(self):
        return self.get("Role")

    @property
    def damage_type(self):
        return self.get("DamageType")

    @property
    def production_cost(self):
        return self.get("uiProductionCost")

    @property
    def item_cost(self):
        return self.get("ItemCost")
