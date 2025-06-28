import os.path
from xml.etree.ElementTree import ElementTree
from PIL import Image


def extract_atlas_images(
    *,
    output_dir: str,
    xml_path: str,
    size: tuple[int, int] = None,
):
    with open(xml_path) as f, Image.open(xml_path.replace(".xml", ".dds")) as image:
        tree = ElementTree().parse(f)

        for entry in tree.find("Entries").iterfind("Entry"):
            id = entry.get("ID")
            width = int(entry.get("Width"))
            height = int(entry.get("Height"))
            (x, y) = [int(num) for num in entry.get("Position").split(",", 1)]

            cropped = image.crop([x, y, x + width, y + height])

            if size:
                cropped = cropped.resize(size)

            cropped.save(os.path.join(output_dir, f"{id}.png"), optimize=True)
