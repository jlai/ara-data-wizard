import math
import types
from exporters.wiki.base import (
    WikiPageUpdater,
)
from mwparserfromhell.wikicode import Template

from littletable import Table
from game_data.database import has_flag
from game_data.eras import ERA_RANKS

FORCE_DOMAINS = {
    "RulesTypes.FormationType.Land": types.SimpleNamespace({"name": "Land"}),
    "RulesTypes.FormationType.Sea": types.SimpleNamespace({"name": "Sea"}),
    "RulesTypes.FormationType.Air": types.SimpleNamespace({"name": "Air"}),
}

ROLE_NAMES = {
    "RulesTypes.UnitRoles.Civilian": "Civilian",
    "RulesTypes.UnitRoles.MeleeInfantry": "Melee Infantry",
    "RulesTypes.UnitRoles.MeleeCavalry": "Melee Cavalry",
    "RulesTypes.UnitRoles.Projectile": "Projectile",
    "RulesTypes.UnitRoles.GunpowderInfantry": "Gunpowder Infantry",
    "RulesTypes.UnitRoles.GunCavalry": "Gun Cavalry",
    "RulesTypes.UnitRoles.Artillery": "Artillery",
    "RulesTypes.UnitRoles.ModernInfantry": "Modern Infantry",
    "RulesTypes.UnitRoles.Armor": "Armor",
    "RulesTypes.UnitRoles.Warship": "Warship",
    "RulesTypes.UnitRoles.Transport": "Transport",
    "RulesTypes.UnitRoles.CannonShip": "Cannon Ship",
    "RulesTypes.UnitRoles.Submarine": "Submarine",
    "RulesTypes.UnitRoles.Destroyer": "Destroyer",
    "RulesTypes.UnitRoles.Battleship": "Battleship",
    "RulesTypes.UnitRoles.Carrier": "Carrier",
    "RulesTypes.UnitRoles.Fighter": "Fighter",
    "RulesTypes.UnitRoles.Bomber": "Bomber",
    "RulesTypes.UnitRoles.Helicopter": "Helicopter",
    "RulesTypes.UnitRoles.Support": "Support",
    "RulesTypes.UnitRoles.AnyMilitary": "Any Military",
}


class UnitsPageUpdater(WikiPageUpdater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_unit_projects = self.db.city_unit_projects.create_index(
            "UnitItemCreated", unique=True
        )
        self.army_game_rules = self.db.all_objects.where(
            _type="ArmyGameRulesDef"
        ).where(id="Root")[0]
        self.damage_types_strings = self.army_game_rules.DamageTypesStrings

    def create_unit_template(self, unit):
        name = self.db.get_text(unit.Name)

        wiki_id = self.get_wiki_id(name)

        recipe_id = self.get_unit_recipe_id(unit)
        recipe = self.db.recipes.by.id[recipe_id]
        unit_item_id = recipe.ItemCreated
        project = self.city_unit_projects.by.UnitItemCreated[unit_item_id]

        tech_ids = self.db.get_techs_that_unlock(recipe_id)

        earliest_era = self.db.eras.by.id[self.db.get_earliest_era_id(recipe_id)]
        earliest_era_name = self.db.get_text(earliest_era.nameKey)

        template = Template(f"UnitsTableRow\n")
        template.add(
            "itemfile", f"{self.get_wiki_icon(wiki_id, "Unit")}\n"
        )  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)
        template.add("Role", ROLE_NAMES[unit.Role])
        template.add(
            "DamageType",
            self.db.get_text(self.damage_types_strings[unit.DamageType]["name"]),
        )
        template.add("EraSort", ERA_RANKS[earliest_era.id])
        template.add("Era", earliest_era_name)
        template.add(
            "Tech",
            "".join(str(self.get_link_template(id)) for id in tech_ids),
        )

        strength = unit.uiBaseStrength
        strength2 = math.floor(strength * 1.175)
        strength3 = math.floor(strength * 1.175 * 1.15)

        template.add("Strength1", strength)
        template.add("Strength2", strength2)
        template.add("Strength3", strength3)

        template.add("Speed", unit.uiBaseSpeed)
        template.add("Range", unit.uiBombardRange)
        template.add(
            "Cost",
            self.describe_item_costs(
                project.ItemCost, production_cost=project.uiProductionCost
            ),
        )
        template.add("Maintenance", self.describe_item_costs(unit.MaintenanceCost))

        notes = []
        if unit.uiBaseReligionStrength:
            notes.append(f"{unit.uiBaseReligionStrength} spread religion")

        if has_flag(unit, "Actions.CanNavigateCoast") and not has_flag(
            unit, "Actions.CanNavigateOcean"
        ):
            notes.append("Coastal only")

        template.add("Notes", "<br />".join(notes))

        return template

    def get_unit_recipe_id(self, unit):
        item_id = list(unit.ConstructionCost.keys())[0]
        item = self.db.items.by.id[item_id]
        return item.RecipeID

    def get_unit_era(self, unit):
        return self.db.get_earliest_era_id(self.get_unit_recipe_id(unit))

    def write_units(self, *, output_filename):
        code = ""

        all_units = self.db.units.where(
            lambda unit: not has_flag(unit, "Actions.ItemToCreateNotRequired")
        )
        all_units.create_index("Type")

        for i, (domain_id, domain) in enumerate(FORCE_DOMAINS.items()):
            domain_header = Template("UnitsTableDomain")
            domain_header.add(
                "Domain",
                f"""<div id="{domain.name}" style="display:inline;">[[#{domain.name}|{domain.name}]]</div>""",
            )

            if i > 0:
                code += "|}"

            code += "\n" + str(domain_header) + "\n"

            for unit in sorted(
                all_units.by.Type[domain_id],
                key=lambda unit: unit.uiBaseStrength,
            ):
                code += str(self.create_unit_template(unit)) + "\n"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)
