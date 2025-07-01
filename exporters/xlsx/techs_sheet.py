from game_data.database import get_tech_obsoletes_ids, get_tech_unlocks_ids
from .base import SheetGenerator, ColumnTemplate
from game_data.eras import ERA_RANKS
from littletable import Table


class TechsSheetGenerator(SheetGenerator):
    COLUMNS = [
        ColumnTemplate("Name"),
        ColumnTemplate("Research cost"),
        ColumnTemplate("Improvements\n(* = unique to this tech)"),
        ColumnTemplate("Goods"),
        ColumnTemplate("Resources"),
        ColumnTemplate("Units"),
        ColumnTemplate("Formations"),
        ColumnTemplate("Special"),
        ColumnTemplate("Obsoletes"),
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
        "Returns a set() of ids that are only unlocked by this tech"

        unlocks_ids = get_tech_unlocks_ids(tech)

        unlocked_elsewhere = (
            self.db.unlocks.where(unlocks_id=Table.is_in(unlocks_ids))
            .where(tech_id=Table.ne(tech.id))
            .all.unlocks_id
        )

        return set(unlocks_ids) - set(unlocked_elsewhere)

    def write_tech(self, tech):
        unlocks_ids = get_tech_unlocks_ids(tech)

        unique_unlocks = self.get_unique_unlocks(tech)

        improvements = []
        units = []
        items = []
        formations = []
        resources = []
        special = []

        for id in unlocks_ids:
            prefix = id.split("_", 1)[0]
            name = self.db.get_name_text(id)
            desc = f"{name} *" if id in unique_unlocks else name

            match prefix:
                case "imp":
                    improvements.append(desc)
                case "frm":
                    formations.append(desc)
                case "itm":
                    resources.append(desc)
                case "rcp":
                    recipe = self.db.recipes.by.id[id]
                    product_id = self.db.get_recipe_product(recipe)
                    if product_id.startswith("unt_"):
                        units.append(desc)
                    else:
                        items.append(desc)
                case _:
                    special.append(desc)

        obsoletes = sorted(
            self.db.get_name_text(id) for id in get_tech_obsoletes_ids(tech)
        )

        self.write_row(
            [
                self.get_text(tech.Name),
                tech.uiResearchCost,
                "\n".join(improvements),
                "\n".join(items),
                "\n".join(resources),
                "\n".join(units),
                "\n".join(formations),
                "\n".join(special),
                "\n".join(obsoletes),
            ]
        )
