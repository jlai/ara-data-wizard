from exporters.wiki.base import (
    WikiPageUpdater,
)
from mwparserfromhell.wikicode import Template

from game_data.database import get_tech_obsoletes_ids, is_improvement_a_triumph
from game_data.zdata.utils import has_flag


def is_transition_tech(tech):
    return has_flag(tech, "TechFlags.CapstoneTech")


class TechsPageUpdater(WikiPageUpdater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_tech_template(self, tech):
        name = self.db.get_text(tech.Name)

        wiki_id = self.get_wiki_id(name)

        template = Template(f"TechTableRow\n")
        template.add(
            "itemfile", f"{self.get_wiki_icon(wiki_id, "Tech")}\n"
        )  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)
        template.add("Cost", tech.uiResearchCost)

        triumph_ids = set(
            id
            for id in tech.UnlockImprovementsIDs
            if is_improvement_a_triumph(self.db.improvements.by.id[id])
        )
        improvement_ids = set(tech.UnlockImprovementsIDs) - triumph_ids
        buildings = [
            self.get_sorted_links(improvement_ids),
            self.get_sorted_links(triumph_ids),
        ]

        template.add("Improvs", "<hr />".join(s for s in buildings if s))

        item_ids = []
        unit_ids = []
        harvested_item_ids = []
        formation_ids = tech.UnlockedFormationsIDs
        government_ids = tech.UnlockGovernmentsIDs
        special_ids = getattr(tech, "UnlockCitySpecialProjects", []) + getattr(
            tech, "UnlockCityMissileProjects", []
        )

        for product_id in (
            self.db.get_recipe_product(self.db.recipes.by.id[recipe_id])
            for recipe_id in tech.UnlockRecipesIDs
        ):
            if product_id.startswith("itm_"):
                item_ids.append(product_id)
            elif product_id.startswith("unt_"):
                unit_ids.append(product_id)

        for unlock in tech.UnlockNaturalResourcesIDs:
            harvested_item_ids.append(unlock["Value"])

        military = []
        if unit_ids:
            military.append(self.get_sorted_links(unit_ids))
        if formation_ids:
            military.append(self.get_sorted_links(formation_ids))

        template.add("CraftGoods", self.get_sorted_links(item_ids))
        template.add("HarvGoods", self.get_sorted_links(harvested_item_ids))
        template.add("Units", "<hr />".join(military))

        special = []

        if is_transition_tech(tech):
            special.append("<div>Age transition</div>")

        for id in government_ids + special_ids:
            special.append(self.get_link_template(id))

        for buff_id in tech.GrantBuffs:
            special.append(f"<div>{self.describe_buff(buff_id)}</div>")

        template.add("Special", "<hr />".join(special))
        template.add(
            "Obsoletes",
            self.get_sorted_links(get_tech_obsoletes_ids(tech), "obsolete"),
        )

        if is_transition_tech(tech):
            template.add("ExtraClasses", "age-transition")

        return template

    def write_techs(self, *, output_filename):
        code = ""
        techs_by_era = {}

        for tech in self.db.techs:
            era_id = tech.Era
            techs_by_era.setdefault(era_id, []).append(tech)

        for era in self.db.eras.orderby("rank"):
            era_name = self.db.get_text(era.nameKey)
            era_wiki_id = self.get_wiki_id(era_name)

            era_header = Template("TechTableAge")
            era_header.add(
                "Age",
                f"""<div id="{era_wiki_id}" style="display:inline;">[[#{era_name}|{era_name}]]</div>""",
            )

            if era.id != "RulesTypes.TechEras.AncientEra":
                code += "|}"

            code += "\n" + str(era_header) + "\n"

            for tech in sorted(
                techs_by_era[era.id],
                key=lambda tech: (
                    1 if is_transition_tech(tech) else 0,
                    self.db.get_name_text(tech.id),
                ),
            ):
                code += str(self.create_tech_template(tech)) + "\n"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)
