import functools
import click
import os

from exporters.graphviz import export_to_graphviz
from game_data.images import extract_atlas_images
from cli.config import json_config
from cli.base import asset_dir_option, cli, ensure_directory, load_database
from exporters.json import ExportJsonOptions, JsonFilter, generate_json
from exporters.xlsx import generate_xlsx
from game_data.database import GameDatabase


@cli.command()
@load_database
@click.option(
    "-o", "output_filename", help="Output filename", default="out/Ara Game Data.xlsx"
)
def excel(*, output_filename, db):
    """Create a XLSX file with various data from the game."""

    ensure_directory(output_filename)
    generate_xlsx(output_filename, db)

    click.echo(f"Spreadsheet written to {output_filename}")


@cli.group
def json():
    pass


def json_options(func):
    @click.option(
        "-o", "output_filename", help="Output filename", default="out/ara-data.json"
    )
    @click.option(
        "--groups",
        help="List of GameCoreData groups to include",
        default=json_config.get("groups", None),
    )
    @click.option(
        "--translate-text",
        help="Convert fields with text keys into localized strings (English)",
        default=json_config.get("translate-text", False),
    )
    @click.option(
        "--normalize-case",
        help="Ensure that properties start with a lower case letter",
        default=json_config.get("normalize-case", True),
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@json.command()
@load_database
@json_options
def dump(
    *,
    output_filename,
    translate_text,
    normalize_case,
    groups,
    db: GameDatabase,
):
    """Dump the game data as a JSON file"""
    options = ExportJsonOptions(
        groups=groups,
        translate_text=translate_text,
        normalize_case=normalize_case,
        filters=[JsonFilter.from_json(rule) for rule in json_config.get("filters", [])],
    )

    ensure_directory(output_filename)
    generate_json(output_filename, db, options)

    click.echo(f"Data written to {output_filename}")


@cli.command()
@load_database
@click.option(
    "-o", "output_filename", help="Output filename", default="out/Ara Goods.svg"
)
def graphviz(
    *,
    output_filename,
    db: GameDatabase,
):
    """Visualize goods dependencies using graphviz"""
    ensure_directory(output_filename)
    export_to_graphviz(output_filename, db, assets_dir=db.assets_dir)

    click.echo(f"Graph written to {output_filename}")


@cli.command()
@asset_dir_option
@click.argument("image_path")
@click.option("-o", "output_dir", help="Output directory", default="out/images")
def images(*, assets_dir, image_path, output_dir):
    """Extract images from image atlas"""
    full_path = os.path.join(assets_dir, image_path)

    ensure_directory(output_dir + "/")
    extract_atlas_images(
        xml_path=full_path,
        output_dir=output_dir,
    )

    click.echo(f"Images written to {output_dir}")
