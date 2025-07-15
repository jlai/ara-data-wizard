from itertools import zip_longest
from natsort import natsorted

from game_data.objects import Improvement

from .base import SheetGenerator, ColumnTemplate
from game_data.eras import ERA_RANKS


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
                improvements.orderby(lambda imp: imp.get_name())
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

    def get_crafting_outputs(self, improvement: Improvement):
        outputs = []

        for recipe in improvement.recipes:
            outputs.append(self.get_text(recipe.product.name, count="other"))

        return outputs

    def get_crafting_inputs(self, improvement: Improvement):
        inputs = set()

        for recipe in improvement.recipes:
            for ingredient in recipe.ingredients:
                for item_id in ingredient.options.keys():
                    if item_id == "itm_Money":
                        continue

                    item = self.db.items.by.id[item_id]
                    name = item.get_name(count="other")
                    inputs.add(name)

        return list(inputs)

    def get_supply_options(self, improvement: Improvement):
        slot_descs = []

        for slot in improvement.supply_slots:
            slot_descs.append(" / ".join(item.get_name() for item in slot.item_choices))
        return slot_descs

    def write_improvements(self, improvements):
        for improvement in improvements:
            self.write_improvement(improvement)

    def write_improvement(self, improvement: Improvement):
        build_cost = self.db.get_item_quantities(
            improvement.get("BuildImprovementItemCost")
        )

        previous_level = improvement.get("PrevLevelID")
        upgrade_info = ""

        if previous_level:
            previous_improvement = self.db.improvements.by.id[previous_level]
            upgrade_cost = self.db.get_item_quantities(
                improvement.get("UpgradeToImprovementItemCost")
            )
            upgrade_info = "\n".join(
                [
                    f"Upgrade from {self.get_text(previous_improvement.name)}\n",
                    *upgrade_cost,
                ]
            )

        worker_slots = improvement.get("WorkerSlots")
        slot_descs = []
        for i, slot in zip_longest(range(1, 5), worker_slots[0:4]):
            if slot:
                buffs = self.db.get_buffs_by_ids(slot["Buffs"])
                slot_descs.append("\n".join(self.describe_buffs(buffs)))
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
                improvement.get_name(),
                "\n".join([tech.get_name() for tech in improvement.unlocked_by]),
                improvement.nation_max_count or "",
                improvement.province_max_count or "",
                *slot_descs,
                "\n".join(sorted(self.get_crafting_outputs(improvement))),
                "\n".join(sorted(self.get_crafting_inputs(improvement))),
                "\n".join(sorted(self.get_supply_options(improvement))),
                improvement.production_cost,
                "\n".join(natsorted(build_cost)),
                upgrade_info,
                "\n".join(maintainance_costs),
            ],
        )
