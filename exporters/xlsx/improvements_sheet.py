from itertools import zip_longest
from natsort import natsorted

from .base import SheetGenerator, ColumnTemplate
from game_data.eras import ERA_RANKS
from game_data.modifiers import get_modifier_text_params


class ImprovementsSheetGenerator(SheetGenerator):
    COLUMNS = [
        ColumnTemplate("Name"),
        ColumnTemplate("Unlocked by"),
        ColumnTemplate("Nation\nmax"),
        ColumnTemplate("City max"),
        ColumnTemplate("Base modifiers", align="left"),
        ColumnTemplate("1 expert", align="left"),
        ColumnTemplate("2 experts", align="left"),
        ColumnTemplate("3 experts", align="left"),
        ColumnTemplate("Crafting outputs"),
        ColumnTemplate("Crafting inputs"),
        ColumnTemplate("Supply items"),
        ColumnTemplate("⚙️ Cost"),
        ColumnTemplate("Build cost"),
        ColumnTemplate("Upgrade cost"),
        ColumnTemplate("Maintenance cost"),
    ]

    def __init__(self, *args):
        super().__init__(*args)

    def create(self):
        self.setup_header(self.COLUMNS)
        self.write_eras()
        self.finish()

    def write_eras(self):
        improvements_by_era = {}
        for era_id, improvements in self.db.improvements.groupby(
            lambda improvement: self.db.get_earliest_era_id(improvement.id), sort=True
        ):
            improvements_by_era[era_id] = list(
                improvements.orderby(lambda imp: self.get_text(imp.Name))
            )

        for era in self.db.eras.orderby(key=lambda era: ERA_RANKS[era.id]):
            self.write_section_header(self.get_text(era.nameKey))
            self.write_improvements(improvements_by_era[era.id])

        self.write_section_header("Special")
        self.write_improvements(improvements_by_era[""])

    def get_recipe_name_by_id(self, recipe_id: str):
        recipe = self.db.recipes.by.id[recipe_id]
        item = self.db.items.by.id[recipe.ItemCreated]
        return self.get_text(item.Name, count="other")

    def get_crafting_outputs(self, improvement):
        outputs = []

        for recipe_id in improvement.Recipes:
            recipe = self.db.recipes.by.id[recipe_id]
            item = self.db.items.by.id[recipe.ItemCreated]
            outputs.append(self.get_text(item.Name, count="other"))

        return outputs

    def get_crafting_inputs(self, improvement):
        inputs = set()

        for recipe_id in improvement.Recipes:
            recipe = self.db.recipes.by.id[recipe_id]

            for ingredient in recipe.Ingredients:
                for item_id in ingredient["Options"].keys():
                    if item_id == "itm_Money":
                        continue

                    item = self.db.items.by.id[item_id]
                    name = self.get_text(item.Name, count="other")
                    inputs.add(name)

        return list(inputs)

    def get_supply_options(self, improvement):
        slots = improvement.ItemOptions
        slot_descs = []

        for slot in slots:
            options = slot["Options"].keys()
            slot_descs.append(
                " / ".join(
                    self.get_text(self.db.items.by.id[item_id].Name)
                    for item_id in options
                )
            )
        return slot_descs

    def write_improvements(self, improvements):
        for improvement in improvements:
            self.write_improvement(improvement)

    def write_improvement(self, improvement):
        build_cost = self.db.get_item_quantities(improvement.BuildImprovementItemCost)

        previous_level = improvement.PrevLevelID
        upgrade_info = ""

        if previous_level:
            previous_improvement = self.db.improvements.by.id[previous_level]
            upgrade_cost = self.db.get_item_quantities(
                improvement.UpgradeToImprovementItemCost
            )
            upgrade_info = "\n".join(
                [
                    f"Upgrade from {self.get_text(previous_improvement.Name)}\n",
                    *upgrade_cost,
                ]
            )

        techs = (
            self.db.unlocks.where(unlocks_id=improvement.id)
            .join(self.db.techs, tech_id="id")
            .orderby("era_rank")
        )

        worker_slots = improvement.WorkerSlots
        slot_descs = []
        for i, slot in zip_longest(range(1, 5), worker_slots[0:4]):
            if slot:
                descs = self.describe_buffs(slot["Buffs"])
                slot_descs.append("\n".join(descs))
            else:
                slot_descs.append("")

        maintainance_costs = []
        for i, slot in enumerate(worker_slots):
            cost = "\n".join(
                natsorted(self.db.get_item_quantities(slot["Maintenance"]))
            )

            if len(maintainance_costs) > 0 and maintainance_costs[-1] == cost:
                continue

            maintainance_costs.append(f"\nWith {i} experts:\n{cost}" if i > 0 else cost)

        self.write_row(
            [
                self.get_text(improvement.Name),
                "\n".join([self.get_text(tech.Name) for tech in techs]),
                improvement.uiNationMaxCount or "",
                improvement.uiProvinceMaxCount or "",
                *slot_descs,
                "\n".join(sorted(self.get_crafting_outputs(improvement))),
                "\n".join(sorted(self.get_crafting_inputs(improvement))),
                "\n".join(sorted(self.get_supply_options(improvement))),
                improvement.uiProductionCost,
                "\n".join(natsorted(build_cost)),
                upgrade_info,
                "\n".join(maintainance_costs),
            ],
        )
