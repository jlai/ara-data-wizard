from game_data.database import get_tech_unlocks_ids
from .base import SheetGenerator, ColumnTemplate
from game_data.eras import ERA_RANKS
from littletable import Table


class TechsSheetGenerator(SheetGenerator):
    COLUMNS = [
        ColumnTemplate("Name"),
        ColumnTemplate("Research cost"),
        ColumnTemplate("Unlocked improvements"),
        ColumnTemplate("Unlocked goods"),
        ColumnTemplate("Unlocked resources"),
        ColumnTemplate("Unlocked units"),
        ColumnTemplate("Unlocked formations"),
        ColumnTemplate("Unique to this tech"),
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

    def get_unique_unlocks(self, tech):
        unlocks_ids = get_tech_unlocks_ids(tech)

        unlocked_elsewhere = (
            self.db.unlocks.where(unlocks_id=Table.is_in(unlocks_ids))
            .where(tech_id=Table.ne(tech.id))
            .all.unlocks_id
        )

        return set(unlocks_ids) - set(unlocked_elsewhere)

    def write_tech(self, tech):
        unlocked_improvements = sorted(
            self.get_text(self.db.improvements.by.id[id].Name)
            for id in tech.UnlockImprovementsIDs
        )

        unlocked_units = []
        unlocked_items = []
        for recipe_id in tech.UnlockRecipesIDs:
            id, name = self.db.get_recipe_product(recipe_id)
            if id.startswith("unt_"):
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

        unique_unlocks = sorted(
            self.db.get_name_text(id) for id in self.get_unique_unlocks(tech)
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
                "\n".join(unique_unlocks),
            ]
        )
