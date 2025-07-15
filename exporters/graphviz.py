import graphviz
import os.path
from game_data.database import GameDatabase
from game_data.eras import ERA_RANKS
from game_data.images import extract_atlas_images
from game_data.objects import Item


def export_to_graphviz(
    output_filename: str,
    db: GameDatabase,
    *,
    assets_dir: str = None,
    for_era="RulesTypes.TechEras.FutureAge",
):
    extension = os.path.splitext(output_filename)[1].lstrip(".")

    dot = graphviz.Digraph(
        "goods",
        comment="Ara Goods",
        format=extension,
        engine="dot",
        graph_attr={"rankdir": "LR", "ranksep": "1"},
        node_attr={"shape": "egg", "fontname": "AvantGarde-Book", "fontsize": "20pt"},
        edge_attr={"labeldistance": "7"},
    )

    included_item_ids = set()
    item_colors = {}

    item: Item
    for item in db.items:
        era_id = db.get_earliest_era_id(item.recipe_id) or db.get_earliest_era_id(
            item.id
        )
        era_rank = ERA_RANKS.get(era_id) or 0

        if (
            item.is_unit
            or not (item.has_flag("Flags.Craftable") or item.has_flag("Flags.Resource"))
            or item.id == "itm_Money"
            or item.id == "itm_Energy"
            or era_rank > ERA_RANKS[for_era]
            or not item.name.startswith("TXT_")
        ):
            continue

        color = ""
        if item.has_flag("Flags.Resource"):
            # Raw resources
            color = "burlywood"
        elif item.get("ActivateBuffs") or item.get("ActivateBuffsForImprovements"):
            # Items with buffs
            color = "darkolivegreen4"
        else:
            # Raw resources
            color = "cornflowerblue"

        item_colors[item.id] = color

        name = db.get_name_text(item.id)
        dot.node(
            item.id,
            f"""<<table border="0"><tr><td>{name}</td></tr><tr><td><img src="graphvis_images/items/{item.get("AtlasID")}.png"/></td></tr></table>>""",
            color=color,
        )

        included_item_ids.add(item.id)

    edges = []
    for recipe in db.recipes:
        product_id = recipe.product.id
        if product_id not in included_item_ids:
            continue

        for ingredient in recipe.ingredients:
            for item_id in ingredient.options.keys():
                if item_id not in included_item_ids:
                    continue
                edges.append((item_id, product_id))
                dot.edge(
                    item_id,
                    product_id,
                    color=item_colors[item_id],
                    labelfontcolor=item_colors[item_id],
                    headlabel=db.items.by.id[item_id].get_name(),
                )

    # Create images
    image_directory = os.path.join(
        os.path.dirname(output_filename), "graphvis_images/items"
    )

    os.makedirs(image_directory, exist_ok=True)

    xml_path = os.path.join(assets_dir, "UI/Art/Icons/Items_160.xml")

    extract_atlas_images(
        output_dir=image_directory,
        xml_path=xml_path,
        size=(80, 80),
    )

    dot.render(f"{os.path.splitext(output_filename)[0]}.gv", outfile=output_filename)
