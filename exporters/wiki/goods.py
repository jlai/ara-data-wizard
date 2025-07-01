from typing import Iterable
from exporters.wiki.base import (
    WikiPageUpdater,
    create_anonymous_template,
    fetch_page_code,
)
from mwparserfromhell.wikicode import Template

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
                lambda item: "Flags.Craftable" in item.Flags
                or "Flags.Warhead" in item.Flags
                and "Flags.Weapon" not in item.Flags
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

        wiki_id = name.replace(" ", "")

        template = Template(f"{GOODS_TEMPLATE_NAME}\n")
        template.add("itemfile", f"{wiki_id}.png\n")  # establish newline convention
        template.add("anchorId", wiki_id)
        template.add("itemname", name)

        # Accelerators
        recipe = self.db.recipes.by.id[item.RecipeID] if item.RecipeID else None
        if recipe:
            for accel_num in range(1, 4):
                ingredient = (
                    recipe.Ingredients[accel_num - 1]
                    if len(recipe.Ingredients) >= accel_num
                    else None
                )
                if not ingredient:
                    template.add(f"Accel{accel_num}", "")
                    continue

                production_bonus = ingredient["ProductionBonus"]
                accel_options = []

                for option_item_id, quantity in ingredient["Options"].items():
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
                for unlock in self.db.unlocks.where(unlocks_id=item.RecipeID).orderby(
                    "era_rank"
                )
            ),
        )

        return template

    def update_page(self, *, output_filename):
        code = fetch_page_code("List_of_Goods")

        template: Template
        for template in code.filter_templates():
            if template.name.matches(GOODS_TEMPLATE_NAME):
                name = (
                    str(template.get("itemname").value).replace("<br />", " ").strip()
                )

                if name == "Heavy Plow":
                    name = "Heavy Plows"

                if name == "Rubber":
                    code.remove(template)
                    continue

                item = self.find_item_by_name(name)

                if item:
                    updated = self.create_goods_template(item)
                    template.update(
                        dict(
                            (str(param.name), param.value) for param in updated.params
                        ),
                        preserve_spacing=False,
                    )

            if template.name.matches("GoodsHarv") and template.get(
                "anchorId"
            ).value.matches("Oil"):
                code.insert_after(
                    template,
                    """
{{GoodsHarv
|itemfile=Rubber.png
|anchorId=Rubber
|itemname=Rubber
|fromNode=
|canAccel=
|other=
}}
""",
                )

        if output_filename == "-":
            print(code)
        else:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(str(code))
