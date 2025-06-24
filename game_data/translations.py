import glob
import numbers
import os
import re
from xml.etree import ElementTree

INTERPOLATE_PATTERN = re.compile(
    r"\{(?P<key>[0-9A-Za-z_\-]+)( \{(?P<count>[\#0-9A-Za-z_\-]+)\})?\}"
)
HREF_PATTERN = re.compile(r"/href:[^/]*/(?P<text>[^/]*?)/Endhref/( /i:(?P<icon>.*?)/)?")
WHITESPACE = re.compile(r"\s+")


class LocalizedLine:
    def __init__(self, key, text_cases: dict[str, str]):
        self.key = key
        self.text_cases = text_cases

    @classmethod
    def from_element(cls, line_el: ElementTree.Element):
        try:
            key = line_el.get("Key")
            plural_els = line_el.find("Plural")

            if plural_els:
                text_cases = {}
                for text_el in plural_els.findall("Text"):
                    text_cases[text_el.get("case")] = text_el.text

                return cls(key, text_cases)
            else:
                text_el = line_el.find("Text")
                plurality_el = line_el.find("Plurality")

                if plurality_el is None:
                    text_cases = {"other": text_el.text or ""}
                else:
                    cases = plurality_el.text.split("|")
                    texts = text_el.text.split("|")

                    text_cases = dict(zip(cases, texts))

                return cls(key, text_cases)
        except Exception as e:
            raise Exception(f"Error parsing {ElementTree.tostring(line_el)}") from e

    def get_plural(self, count: str | int = 1):
        if count == 0 or count == "0":
            count = 1

        return self.text_cases.get(str(count)) or self.text_cases.get("other")


class LocalizedStrings:
    def __init__(self, locale: str, lines: dict):
        self.locale = locale
        self.lines: dict[str, LocalizedLine] = lines

    def interpolate(self, line: LocalizedLine, *, count: int = 1, params: dict = {}):
        def replace_link(match: re.Match[str]):
            return match.group("text")

        def replace(match: re.Match[str]):
            sub_count = 1
            key = match.group("key")

            count_str = match.group("count")
            count_str = count_str.lstrip("#") if count_str else None

            if count_str and count_str.isnumeric():
                sub_count = int(count_str)

            if key in params:
                value = params[key]
                if isinstance(value, numbers.Number):
                    return f"{value:10g}"

                return str(value)
            else:
                sub_line = self.lines.get(key)
                if sub_line:
                    return sub_line.get_plural(sub_count)

            return f"?{key}?"

        template = line.get_plural(count)

        while INTERPOLATE_PATTERN.search(template):
            template = HREF_PATTERN.sub(replace_link, template)
            template = INTERPOLATE_PATTERN.sub(replace, template)

        # Consolidate whitespace
        template = WHITESPACE.sub(" ", template).strip()

        return template


def parse_translation_file(path):
    with open(path, "r", encoding="utf-8") as f:
        tree = ElementTree.parse(f)

        locale = tree.find("Locale").attrib["ID"]
        lines = {}

        for line_el in tree.iter("Line"):
            line = LocalizedLine.from_element(line_el)
            lines[line.key] = line

        return LocalizedStrings(locale, lines)


def get_english_translations(assets_dir: str):
    lines = {}

    for path in glob.glob("Text/en/*.xml", root_dir=assets_dir):
        locale_data = parse_translation_file(os.path.join(assets_dir, path))
        lines.update(locale_data.lines)

    return LocalizedStrings("en", lines)
