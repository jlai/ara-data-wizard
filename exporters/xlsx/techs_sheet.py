from .base import SheetGenerator, ColumnTemplate
from game_data.eras import ERA_RANKS
from game_data.modifiers import get_modifier_text_params


class TechsSheetGenerator(SheetGenerator):
    COLUMNS = [
        ColumnTemplate("Name"),
        ColumnTemplate("Research cost"),
        ColumnTemplate("Unlocked improvements"),
        ColumnTemplate("Unlocked goods"),
        ColumnTemplate("Unlocked resources"),
        ColumnTemplate("Unlocked units"),
        ColumnTemplate("Unlocked formations"),
        ColumnTemplate("Unlocked governments"),
    ]

    def __init__(self, *args):
        super().__init__(*args)

    def create(self):
        self.setup_header(self.COLUMNS)
        self.write_eras()
        self.finish()

    def write_eras(self):
        techs_by_era = {}
        for era_id, techs in self.db.techs.groupby(lambda tech: tech.Era, sort=True):
            techs_by_era[era_id] = list(
                techs.orderby(lambda tech: self.get_text(tech.Name))
            )

        for era in self.db.eras.orderby(key=lambda era: ERA_RANKS[era.id]):
            self.write_section_header(self.get_text(era.nameKey))
            self.write_techs(techs_by_era[era.id])

    def write_techs(self, techs):
        for tech in techs:
            self.write_tech(tech)

    def write_tech(self, tech):
        unlocked_improvements = sorted(
            self.get_text(self.db.improvements.by.id[id].Name)
            for id in tech.UnlockImprovementsIDs
        )

        unlocked_units = []
        unlocked_items = []
        for recipe_id in tech.UnlockRecipesIDs:
            product_type, name = self.db.get_recipe_product(recipe_id)
            if product_type == "unit":
                unlocked_units.append(self.get_text(name))
            else:
                unlocked_items.append(self.get_text(name))

        unlocked_formations = sorted(
            self.get_text(self.db.formations.by.id[id].Name)
            for id in tech.UnlockedFormationsIDs
        )

        unlocked_resources = sorted(
            self.get_text(self.db.items.by.id[obj["Value"]].Name)
            for obj in tech.UnlockNaturalResourcesIDs
        )

        unlocked_governments = sorted(
            self.get_text(self.db.governments.by.id[id].m_Name)
            for id in tech.UnlockGovernmentsIDs
        )

        self.write_row(
            [
                self.get_text(tech.Name),
                tech.uiResearchCost,
                "\n".join(unlocked_improvements),
                "\n".join(unlocked_items),
                "\n".join(unlocked_resources),
                "\n".join(unlocked_units),
                "\n".join(unlocked_formations),
                "\n".join(unlocked_governments),
            ]
        )
