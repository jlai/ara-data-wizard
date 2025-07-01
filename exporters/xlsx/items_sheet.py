from .base import SheetGenerator, ColumnTemplate
from game_data.eras import ERA_RANKS
from game_data.modifiers import get_modifier_text_params


class ItemsSheetGenerator(SheetGenerator):
    COLUMNS = [
        ColumnTemplate("Name"),
        ColumnTemplate("Unlocked by"),
        ColumnTemplate("As city amenity"),
        ColumnTemplate("As supply"),
        ColumnTemplate("Supplies"),
        ColumnTemplate("Used in construction"),
        ColumnTemplate("Production cost ⚙️"),
        ColumnTemplate("Accelerator 1"),
        ColumnTemplate("Accelerator 2"),
        ColumnTemplate("Accelerator 3"),
    ]

    def __init__(self, *args):
        super().__init__(*args)

    def create(self):
        self.setup_header(self.COLUMNS)
        self.write_eras()
        self.finish()

    def write_eras(self):
        items_by_era = {}
        for era_id, items in self.db.items.where(
            lambda item: "Flags.HideUnlessDebug" not in item.Flags
            and not getattr(item, "TargetUnitID", None)
        ).groupby(lambda item: self.db.get_earliest_era_id(item.RecipeID), sort=True):
            items_by_era[era_id] = list(
                items.orderby(lambda item: self.get_text(item.Name))
            )

        for era in self.db.eras.orderby(key=lambda era: ERA_RANKS[era.id]):
            self.write_section_header(self.get_text(era.nameKey))
            self.write_items(items_by_era[era.id])

        self.write_section_header("Raw materials")
        self.write_items(items_by_era[""])

    def write_items(self, items):
        for item in items:
            self.write_item(item)

    def write_item(self, item):
        techs = (
            self.db.unlocks.where(unlocks_id=item.RecipeID)
            .join(self.db.techs, tech_id="id")
            .orderby("era_rank")
        )

        amenity_buffs = self.describe_buffs(getattr(item, "ActivateBuffs", []))
        supply_buffs = self.describe_buffs(
            getattr(item, "ActivateBuffsForImprovements", [])
        )

        supplied_improvements = sorted(
            set(
                self.get_text(supply.improvement_name)
                for supply in self.db.supplies.where(item_id=item.id)
            )
        )

        construction_projects = sorted(
            f"{self.db.get_name_text(record.output_id, count={record.count_needed})} ({record.count_needed})"
            for record in self.db.item_costs.by.item_id[item.id]
        )

        production_cost = ""

        try:
            recipe = self.db.recipes.by.id[item.RecipeID]
        except:
            recipe = None

        accelerators = ["", "", ""]
        if recipe:
            production_cost = recipe.ProductionCost

            for i, ingredient in enumerate((recipe.Ingredients or [])[0:3]):
                accelerators[i] = (
                    " /\n".join(self.db.get_item_quantities(ingredient["Options"]))
                    + f"\n\n{ingredient['ProductionBonus']:+g} ⚙️"
                )

        self.write_row(
            [
                self.get_text(item.Name),
                "\n".join([self.get_text(tech.Name) for tech in techs]),
                "\n".join(amenity_buffs),
                "\n".join(supply_buffs),
                "\n".join(supplied_improvements),
                "\n".join(construction_projects),
                production_cost,
                *accelerators,
            ]
        )
