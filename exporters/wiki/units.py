import math
import types
from exporters.wiki.base import (
    WikiPageUpdater,
)
from mwparserfromhell.wikicode import Template

from game_data.eras import ERA_RANKS
from game_data.objects import Unit

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
        self.army_game_rules = self.db.get_object_table("GameRules").by.id[
            "ArmyGameRules"
        ]
        self.damage_types_strings = self.army_game_rules.get("DamageTypesStrings")

    def create_unit_template(self, unit: Unit):
        name = unit.get_name()

        wiki_id = self.get_wiki_id(name)

        recipe = unit.recipe
        project = unit.project

        tech_ids = [tech.id for tech in recipe.unlocked_by]

        earliest_era = self.db.eras.by.id[self.db.get_earliest_era_id(recipe.id)]
        earliest_era_name = self.db.get_text(earliest_era.nameKey)

        template = Template(f"UnitsTableRow\n")
        template.add(
            "itemfile", f"{self.get_wiki_icon(wiki_id, "Unit")}\n"
        )  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)
        template.add("Role", ROLE_NAMES[unit.role])
        template.add(
            "DamageType",
            self.db.get_text(self.damage_types_strings[unit.damage_type]["name"]),
        )
        template.add("EraSort", ERA_RANKS[earliest_era.id])
        template.add("Era", earliest_era_name)
        template.add(
            "Tech",
            "".join(str(self.get_link_template(id)) for id in tech_ids),
        )

        strength = unit.base_strength
        strength2 = math.floor(strength * 1.175)
        strength3 = math.floor(strength * 1.175 * 1.15)

        template.add("Strength1", strength)
        template.add("Strength2", strength2)
        template.add("Strength3", strength3)

        template.add("Speed", unit.base_speed)
        template.add("Range", unit.bombard_range)
        template.add(
            "Cost",
            self.describe_item_costs(
                project.get("ItemCost"), production_cost=project.get("uiProductionCost")
            ),
        )
        template.add(
            "Maintenance", self.describe_item_costs(unit.get("MaintenanceCost"))
        )

        notes = []
        if unit.base_religion_strength:
            notes.append(f"{unit.base_religion_strength} spread religion")

        if unit.has_flag("Actions.CanNavigateCoast") and not unit.has_flag(
            "Actions.CanNavigateOcean"
        ):
            notes.append("Coastal only")

        template.add("Notes", "<br />".join(notes))

        return template

    def get_unit_era(self, unit):
        return self.db.get_earliest_era_id(unit.recipe.id)

    def write_units(self, *, output_filename):
        code = ""

        all_units = self.db.units.where(
            lambda unit: not unit.has_flag("Actions.ItemToCreateNotRequired")
        )
        all_units.create_index("type")

        for i, (domain_id, domain) in enumerate(FORCE_DOMAINS.items()):
            domain_header = Template("UnitsTableDomain")
            domain_header.add(
                "Domain",
                f"""<div id="{domain.name}" style="display:inline;">[[#{domain.name}|{domain.name}]]</div>""",
            )

            if i > 0:
                code += "|}"

            code += "\n" + str(domain_header) + "\n"

            unit: Unit
            for unit in sorted(
                all_units.by.type[domain_id],
                key=lambda unit: unit.base_strength,
            ):
                code += str(self.create_unit_template(unit)) + "\n"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)
