from pprint import pp
import unicodedata
import mwparserfromhell
from mwparserfromhell.wikicode import Template
import requests

from game_data.database import GameDatabase
from game_data.modifiers import get_modifier_text_params, parse_modifier_actions
from game_data.objects import Buff, Improvement

BUFF_LINK_TERMS = {
    "City Knowledge": "{{Knowledge}}",
    "City Health": "{{Health}}",
    "City Food": "City Food {{Food}}",
    "City Happiness": "{{Happiness}}",
    "City Prosperity": "{{Prosperity}}",
    "City Security": "{{Security}}",
    "City Production": "City [[Production]]",
    "Craft Production": "[[Craft Production]]",
    "Harvest Production": "[[Harvest Production]]",
    "Improvement": "[[Improvement]]",
    "Research per Turn": "{{Research}} / {{Turn}}",
    "Provides ": "",
}

BASIC_RESOURCE_ITEMS = set(("itm_Money", "itm_Food", "itm_Stone", "itm_Wood"))

DOMAIN_NAMES = {
    "RulesTypes.Domain.Military": "Military",
    "RulesTypes.Domain.Commerce": "Commerce",
    "RulesTypes.Domain.Government": "Government",
    "RulesTypes.Domain.Religion": "Religion",
    "RulesTypes.Domain.Culture": "Culture",
    "RulesTypes.Domain.Science": "Science",
    "RulesTypes.Domain.Industry": "Industry",
    "RulesTypes.Domain.Impact": "Impact",
}


def fetch_page_code(uri: str):
    wikitext = requests.get(f"https://ara.wiki/{uri}?action=raw").text
    code = mwparserfromhell.parse(wikitext)
    return code


def fetch_image_list():
    continue_token = None
    all_files = dict()

    while True:
        params = {
            "action": "query",
            "list": "allimages",
            "ailimit": "500",
            "format": "json",
        }

        if continue_token:
            params["aicontinue"] = continue_token

        response = requests.get(f"https://ara.wiki/api.php", params=params).json()

        for file_info in response.get("query", {}).get("allimages", []):
            all_files[file_info["name"]] = file_info

        continue_token = response.get("continue", {}).get("aicontinue")

        if not continue_token:
            break

    return all_files


def create_anonymous_template(name, *params):
    template = Template(name)
    for i, param in enumerate(params):
        template.add(f"{i+1}", param)
    return template


class WikiPageUpdater:
    def __init__(self, db: GameDatabase):
        self.db = db
        self.wiki_images = fetch_image_list()

    def write_code(self, code, *, output_filename="-"):
        if output_filename == "-":
            print(code)
        else:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(str(code))

    def get_item_link_path(self, item, wiki_id):
        return (
            "List_of_Resource_Nodes#Basic_Resources"
            if item.id in BASIC_RESOURCE_ITEMS
            else f"List_of_Goods#{wiki_id}"
        )

    def get_wiki_icon(self, wiki_id, suffix=None):
        # Look for icons with "Item" suffix first
        if suffix and f"{wiki_id}{suffix}.png" in self.wiki_images:
            return f"{wiki_id}{suffix}.png"
        else:
            return f"{wiki_id}.png"

    def get_sorted_links(self, obj_ids, extra_css_class=""):
        return "".join(
            str(self.get_link_template(obj_id, extra_css_class=extra_css_class))
            for obj_id in sorted(set(obj_ids), key=self.db.get_name_text)
        )

    def get_domain_link(self, domain_id):
        name = DOMAIN_NAMES[domain_id]
        return "{{" + f"Domain{name}" + "}}"

    def get_link_template(self, obj_id, extra_css_class=""):
        prefix = obj_id.split("_", 1)[0]
        name = self.get_wiki_name(self.db.get_name_text(obj_id))
        wiki_id = self.get_wiki_id(name)
        css_class = f"Class{wiki_id}"

        if extra_css_class:
            css_class += f" {extra_css_class}"

        match prefix:
            case "imp":
                improvement: Improvement = self.db.improvements.by.id[obj_id]

                return create_anonymous_template(
                    "TriuIcon" if improvement.is_triumph else "ImpIcon",
                    f"{wiki_id}.png",
                    wiki_id,
                    css_class,
                    name,
                )

            case "tch":
                return create_anonymous_template(
                    "Tech", f"{wiki_id}.png", css_class, name
                )

            case "unt":
                return create_anonymous_template(
                    "UnitIcon", f"{wiki_id}.png", wiki_id, css_class, name
                )

            case "itm":
                item = self.db.items.by.id[obj_id]

                link = self.get_item_link_path(item, wiki_id)
                return create_anonymous_template(
                    "ItemIcon",
                    self.get_wiki_icon(wiki_id, "Item"),
                    link,
                    css_class,
                    name,
                )

            case "nrc":
                return create_anonymous_template(
                    "ItemIcon",
                    self.get_wiki_icon(wiki_id, "Item"),
                    f"List_of_Resource_Nodes#{wiki_id}",
                    css_class,
                    name,
                )

            case "rcp":
                recipe = self.db.recipes.by.id[obj_id]

                return self.get_link_template(
                    recipe.product.id, extra_css_class=extra_css_class
                )

            case "cup":
                project = self.db.city_unit_projects.by.id[obj_id]
                item = self.db.items.by.id[project.unit_item_id]

                return self.get_link_template(
                    item.TargetUnitID, extra_css_class=extra_css_class
                )

            case "gvt":
                return f"<div>[[List_of_Government_Types#{wiki_id}|{name}]]</div>"

            case "frm":
                return f"<div>[[Combat#{wiki_id}|{name}]]</div>"

            case "csp" | "cmp":
                return f"<div>City project: {name}</div>"

            case _:
                raise Exception(f"Unknown object type: {obj_id}")

    def get_wiki_name(self, name):
        return name

    def get_wiki_id(self, name):
        match name:
            case "Himeji-jo":
                return "HimejiJo"
            case "CRISPR":
                return "Crispr"
            case "White-tailed Deer":
                return "WhiteTailedDeer"

            case _:
                name = (
                    name.replace(" ", "")
                    .replace("-", "")
                    .replace("'", "")
                    .replace(".", "")
                )

                # Strip accent marks
                nfkd_form = unicodedata.normalize("NFD", name)
                name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])

        return name

    def describe_buff(self, buff: Buff):
        text = buff.describe()
        for term, replacement in BUFF_LINK_TERMS.items():
            text = text.replace(term, replacement)

        return text

    def describe_item_costs(self, item_costs: dict, production_cost=None):
        descs = []

        if production_cost:
            descs.append(f"<div>{production_cost} {{{{ProdIcon}}}}</div>")

        for item_id, quantity in sorted(item_costs.items(), key=lambda x: x[1]):
            descs.append(
                f"<div>{quantity}x {str(self.get_link_template(item_id))}</div>"
            )

        return " ".join(descs)
