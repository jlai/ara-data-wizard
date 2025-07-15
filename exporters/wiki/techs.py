from exporters.wiki.base import (
    WikiPageUpdater,
)
from mwparserfromhell.wikicode import Template

from game_data.objects import Tech


class TechsPageUpdater(WikiPageUpdater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_tech_template(self, tech: Tech):
        name = tech.get_name()

        wiki_id = self.get_wiki_id(name)

        template = Template(f"TechTableRow\n")
        template.add(
            "itemfile", f"{self.get_wiki_icon(wiki_id, "Tech")}\n"
        )  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)
        template.add("Cost", tech.research_cost)

        triumph_ids = set(
            id
            for id in tech.get("UnlockImprovementsIDs", [])
            if self.db.improvements.by.id[id].is_triumph
        )
        improvement_ids = set(tech.get("UnlockImprovementsIDs", [])) - triumph_ids
        buildings = [
            self.get_sorted_links(improvement_ids),
            self.get_sorted_links(triumph_ids),
        ]

        template.add("Improvs", "<hr />".join(s for s in buildings if s))

        item_ids = []
        unit_ids = []
        harvested_item_ids = []
        formation_ids = tech.get("UnlockFormationIDs", [])
        government_ids = tech.get("UnlockGovernmentsIDs", [])
        special_ids = tech.get("UnlockCitySpecialProjects", []) + tech.get(
            "UnlockCityMissilePorjects", []
        )

        for product_id in (
            self.db.recipes.by.id[recipe_id].product.id
            for recipe_id in tech.get("UnlockRecipesIDs", [])
        ):
            if product_id.startswith("itm_"):
                item_ids.append(product_id)
            elif product_id.startswith("unt_"):
                unit_ids.append(product_id)

        for unlock in tech.get("UnlockNaturalResourcesIDs", []):
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

        if tech.is_transition_tech:
            special.append("<div>Age transition</div>")

        for id in government_ids + special_ids:
            special.append(self.get_link_template(id))

        for buff in tech.buffs:
            special.append(f"<div>{self.describe_buff(buff)}</div>")

        template.add("Special", "<hr />".join(special))
        template.add(
            "Obsoletes",
            self.get_sorted_links(tech.obsoletes_ids, "obsolete"),
        )

        if tech.is_transition_tech:
            template.add("ExtraClasses", "age-transition")

        return template

    def write_techs(self, *, output_filename):
        code = ""
        techs_by_era = {}

        for tech in self.db.techs:
            techs_by_era.setdefault(tech.era_id, []).append(tech)

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
                    1 if tech.is_transition_tech else 0,
                    self.db.get_name_text(tech.id),
                ),
            ):
                code += str(self.create_tech_template(tech)) + "\n"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)
