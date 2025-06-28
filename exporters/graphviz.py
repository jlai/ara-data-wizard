import graphviz
import os.path
from game_data.database import GameDatabase
from game_data.eras import ERA_RANKS


def export_to_graphviz(
    output_filename: str, db: GameDatabase, for_era="RulesTypes.TechEras.FutureAge"
):
    extension = os.path.splitext(output_filename)[1].lstrip(".")

    dot = graphviz.Digraph(
        "goods",
        comment="Ara Goods",
        format=extension,
        engine="dot",
        graph_attr={"rankdir": "LR"},
        node_attr={"shape": "egg"},
    )

    included_item_ids = set()
    item_colors = {}

    for item in db.items:
        era_id = db.get_earliest_era_id(item.RecipeID) or db.get_earliest_era_id(
            item.id
        )
        era_rank = ERA_RANKS.get(era_id) or 0

        if (
            getattr(item, "TargetUnitID", None)
            or not ("Flags.Craftable" in item.Flags or "Flags.Resource" in item.Flags)
            or "HideUnlessDebug" in item.Flags
            or item.id == "itm_Money"
            or item.id == "itm_Energy"
            or era_rank > ERA_RANKS[for_era]
            or not item.Name.startswith("TXT_")
        ):
            continue

        color = ""
        if "Flags.Resource" in item.Flags:
            # Raw resources
            color = "burlywood"
        elif getattr(item, "ActivateBuffs", None) or getattr(
            item, "ActivateBuffsForImprovements"
        ):
            # Items with buffs
            color = "darkolivegreen4"
        else:
            # Raw resources
            color = "cornflowerblue"

        item_colors[item.id] = color

        name = db.get_name_text(item.id)
        dot.node(item.id, name, color=color)

        included_item_ids.add(item.id)

    edges = []
    for recipe in db.recipes:
        product_id = recipe.ItemCreated
        if product_id not in included_item_ids:
            continue

        for ingredient in recipe.Ingredients:
            for item_id in ingredient["Options"].keys():
                if item_id not in included_item_ids:
                    continue
                edges.append((item_id, product_id))
                dot.edge(item_id, product_id, color=item_colors[item_id])

    dot.render(f"{os.path.splitext(output_filename)[0]}.gv", outfile=output_filename)
