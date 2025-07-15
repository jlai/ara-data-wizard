from typing import Iterable
from exporters.wiki.base import (
    WikiPageUpdater,
    create_anonymous_template,
    fetch_page_code,
)
from mwparserfromhell.wikicode import Template

from game_data.eras import ERA_RANKS
from game_data.objects import Recipe

GOODS_TEMPLATE_NAME = "GoodsCraft"


def join_buff_descs(descs: Iterable[str]):
    delimeter = "<br />"
    descs = list(descs)

    # If there's multiple links, join using <hr /> instead
    if any((desc.count("{{") + desc.count("[[")) > 1 for desc in descs):
        delimeter = "<hr />"

    return delimeter.join(descs)


class GoodsPageUpdater(WikiPageUpdater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = (
            self.db.items.where(
                lambda item: (
                    item.has_flag("Flags.Craftable") or item.has_flag("Flags.Warhead")
                )
                and not item.has_flag("Flags.Weapon")
            )
            .compute_field("english_name", lambda item: self.db.get_name_text(item.id))
            .create_index("english_name")
        )

    def find_item_by_name(self, name):
        items = self.items.where(english_name=name)

        match len(items):
            case 1:
                return items[0]
            case _:
                return None

    def create_goods_template(self, item):
        name = item.english_name

        wiki_id = self.get_wiki_id(name)

        template = Template(f"{GOODS_TEMPLATE_NAME}\n")
        template.add(
            "itemfile", f"{self.get_wiki_icon(wiki_id, "Item")}\n"
        )  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)

        # Accelerators
        recipe: Recipe = (
            self.db.recipes.by.id[item.recipe_id] if item.recipe_id else None
        )
        if recipe:
            ingredients = recipe.ingredients

            for accel_num in range(1, 4):
                ingredient = (
                    ingredients[accel_num - 1]
                    if len(ingredients) >= accel_num
                    else None
                )
                if not ingredient:
                    template.add(f"Accel{accel_num}", "")
                    continue

                production_bonus = ingredient.production_bonus
                accel_options = []

                for option_item_id, quantity in ingredient.options.items():
                    option_item = self.db.items.by.id[option_item_id]
                    option_item_name = self.db.get_name_text(option_item_id)
                    option_item_wiki_id = self.get_wiki_id(option_item_name)

                    link = self.get_item_link_path(option_item, option_item_wiki_id)
                    accel = create_anonymous_template(
                        "Accel",
                        quantity,
                        f"{option_item_wiki_id}.png",
                        link,
                        f"Class{option_item_wiki_id}",
                        option_item_name,
                    )
                    accel_options.append(str(accel))

                template.add(
                    f"Accel{accel_num}",
                    f"{production_bonus} {{{{ProdIcon}}}}<hr />{"<br />".join(accel_options)}",
                )

        # Amenity buffs
        template.add(
            "Ameni",
            join_buff_descs(
                self.describe_buff(buff_id)
                for buff_id in getattr(item, "ActivateBuffs", [])
                if buff_id
            ),
        )

        # Supply buffs
        template.add(
            "Suppl",
            join_buff_descs(
                self.describe_buff(buff_id)
                for buff_id in getattr(item, "ActivateBuffsForImprovements", [])
                if buff_id
            ),
        )

        # Crafted in
        if recipe:
            improvement_ids = set(
                entry.improvement_id
                for entry in self.db.crafting_locations.by.item_id[item.id]
            )

            template.add(
                "CraftIn",
                "".join(
                    str(self.get_link_template(improvement_id))
                    for improvement_id in sorted(
                        improvement_ids, key=self.db.get_earliest_era_id
                    )
                ),
            )

        # Used in
        item_products = []
        improvement_products = []
        triumph_products = []
        other_products = []

        output_ids = set(
            entry.output_id for entry in self.db.item_costs.where(input_item_id=item.id)
        )

        for output_id in sorted(
            output_ids,
            key=lambda id: (self.db.get_era_rank(id), self.db.get_name_text(id)),
        ):
            link = str(self.get_link_template(output_id))

            if "ItemIcon" in link:
                item_products.append(link)
            elif "ImpIcon" in link:
                improvement_products.append(link)
            elif "TriuIcon" in link:
                triumph_products.append(link)
            else:
                other_products.append(link)

        template.add(
            "UsedIn",
            "<hr />".join(
                x
                for x in (
                    "".join(item_products),
                    "".join(improvement_products),
                    "".join(triumph_products),
                    "".join(other_products),
                )
                if x
            ),
        )

        # Techs
        template.add(
            "Tech",
            "".join(
                str(self.get_link_template(unlock.tech_id))
                for unlock in self.db.unlocks.where(unlocks_id=item.recipe_id).orderby(
                    "era_rank"
                )
            ),
        )

        return template

    def create_harvested_goods_template(self, item):
        name = item.get_name()

        wiki_id = self.get_wiki_id(name)

        template = Template(f"GoodsHarv\n")
        template.add(
            "itemfile", f"{self.get_wiki_icon(wiki_id, "Item")}\n"
        )  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)

        template.add(
            "fromNode",
            self.get_sorted_links(
                self.db.item_costs.where(
                    output_id=item.id, type="harvest"
                ).all.input_item_id
            ),
        )
        template.add(
            "canAccel",
            self.get_sorted_links(
                self.db.item_costs.where(
                    input_item_id=item.id, type="recipe"
                ).all.output_id
            ),
        )

        template.add(
            "unlockedBy", self.get_sorted_links(tech.id for tech in item.unlocked_by)
        )

        return template

    def generate_goods_code(self, *, output_filename):
        code = ""
        items_by_era = {}

        for item in self.items:
            era_id = self.db.get_earliest_era_id(
                item.recipe_id
            ) or self.db.get_earliest_era_id(item.id)
            items_by_era.setdefault(era_id, []).append(item)

        for era in self.db.eras.orderby(lambda era: ERA_RANKS[era.id]):
            era_name = self.db.get_text(era.nameKey)
            era_wiki_id = self.get_wiki_id(era_name)

            era_header = Template("GoodsAge")
            era_header.add(
                "Age",
                f"""<div id="{era_wiki_id}" style="display:inline;">[[#{era_name}|{era_name}]]</div>""",
            )

            if era.id != "RulesTypes.TechEras.AncientEra":
                code += "|}"

            code += str(era_header) + "\n"

            for item in sorted(
                items_by_era[era.id],
                key=lambda item: self.db.get_name_text(item.id),
            ):
                code += str(self.create_goods_template(item)) + "\n"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)

    def generate_harvested_goods_code(self, *, output_filename):
        code = ""

        for item in self.db.items.where(
            lambda x: x.has_flag("Flags.Resource") and not x.has_flag("Flags.Hidden")
        ).orderby(lambda x: self.db.get_name_text(x.id)):
            code += str(self.create_harvested_goods_template(item)) + "\n"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)

    def update_page(self, *, output_filename):
        code = fetch_page_code("List_of_Goods")

        template: Template
        for template in code.filter_templates(matches=GOODS_TEMPLATE_NAME):
            name = str(template.get("itemname").value).replace("<br />", " ").strip()

            item = self.find_item_by_name(name)

            if item:
                updated = self.create_goods_template(item)
                template.update(
                    dict((str(param.name), param.value) for param in updated.params),
                    preserve_spacing=False,
                )

        self.write_code(code, output_filename=output_filename)
