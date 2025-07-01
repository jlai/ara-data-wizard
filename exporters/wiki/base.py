from pprint import pp
import unicodedata
import mwparserfromhell
from mwparserfromhell.wikicode import Template
import requests

from game_data.database import GameDatabase
from game_data.modifiers import get_modifier_text_params, parse_modifier_actions

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

    def get_link_template(self, obj_id):
        prefix = obj_id.split("_", 1)[0]
        name = self.get_wiki_name(self.db.get_name_text(obj_id))
        wiki_id = self.get_wiki_id(name)

        match prefix:
            case "imp":
                improvement = self.db.improvements.by.id[obj_id]
                is_triumph = "GrantedFlag.Triumph" in (improvement.GrantedFlags or [])

                return create_anonymous_template(
                    "TriuIcon" if is_triumph else "ImpIcon",
                    f"{wiki_id}.png",
                    wiki_id,
                    f"Class{wiki_id}",
                    name,
                )

            case "tch":
                return create_anonymous_template(
                    "Tech", f"{wiki_id}.png", f"Class{wiki_id}", name
                )

            case "unt":
                return create_anonymous_template(
                    "UnitIcon", f"{wiki_id}.png", wiki_id, f"Class{wiki_id}", name
                )

            case "itm":
                item = self.db.items.by.id[obj_id]

                link = self.get_item_link_path(item, wiki_id)
                return create_anonymous_template(
                    "ItemIcon",
                    self.get_wiki_icon(wiki_id, "Item"),
                    link,
                    f"Class{wiki_id}",
                    name,
                )

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

    def describe_buff(self, buff_id):
        buff = self.db.buffs.by.id[buff_id]

        params = get_modifier_text_params(buff.Modifiers)
        text = self.db.get_text(buff.Description, params=params)

        for term, replacement in BUFF_LINK_TERMS.items():
            text = text.replace(term, replacement)

        return text
