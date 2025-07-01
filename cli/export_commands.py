import click
import os

from exporters.graphviz import export_to_graphviz
from game_data.images import extract_atlas_images
from cli.config import json_config
from cli.base import asset_dir_option, cli, ensure_directory, load_database
from exporters.json import ExportJsonOptions, generate_json
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


@cli.command()
@load_database
@click.option(
    "-o", "output_filename", help="Output filename", default="out/ara-data.json"
)
@click.option(
    "--translate-text",
    help="Convert fields with text keys into localized strings (English)",
    default=json_config.get("translate-text", False),
)
@click.option(
    "--remove-properties",
    help="Property names to remove from all objects",
    default=json_config.get("remove-properties", []),
    type=list[str],
)
@click.option(
    "--normalize-case",
    help="Ensure that properties start with a lower case letter",
    default=json_config.get("normalize-case", True),
)
def json(
    *,
    output_filename,
    translate_text,
    remove_properties,
    normalize_case,
    db: GameDatabase,
):
    """Create a JSON file with various data from the game."""
    options = ExportJsonOptions(
        translate_text=translate_text,
        remove_properties=remove_properties,
        normalize_case=normalize_case,
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
