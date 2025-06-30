import functools
from pathlib import PurePath
import sys
import click
import tomllib
import os.path
import glob
from exporters.graphviz import export_to_graphviz
from exporters.json import ExportJsonOptions, generate_json
from exporters.xlsx import generate_xlsx
from game_data.database import GameDatabase
from game_data.images import extract_atlas_images
from game_data.zdata.parse import parse_zdata_file

config = {}

for config_location in [".AraWizard.toml", os.path.expanduser("~/.AraWizard.toml")]:
    if os.path.exists(config_location):
        with open(config_location, "rb") as f:
            config = tomllib.load(f)

json_config = config.get("json", {})


def ensure_directory(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def asset_dir_option(func):
    @click.option(
        "--assets-dir",
        help="Game assets directory path",
        required=True,
        default=config.get("assets-dir"),
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def load_database(func):
    @asset_dir_option
    @click.option(
        "--cache-dir",
        help="Directory for cached data",
        default=config.get("cache-dir") or ".cache",
    )
    @functools.wraps(func)
    def wrapper(*args, assets_dir, cache_dir, **kwargs):
        db = GameDatabase(assets_dir, cache_dir=cache_dir)

        return func(db=db, *args, **kwargs)

    return wrapper


@click.group()
def cli():
    pass


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
@click.option(
    "-d",
    "directory",
    help="Directory to scan",
    required=True,
    default=config.get("mods-dir")
    or os.path.expanduser("~/Documents/My Games/Ara History Untold/Mods"),
)
@click.option("--quiet", help="Keep going on error", type=bool)
@click.option("--keep-going", help="Keep going on error", type=bool)
@click.option(
    "--include",
    help="Only validate files matching a glob pattern, like MyMod/**",
    type=str,
)
@click.option(
    "--exclude", help='Exclude files matching a glob pattern, like "*DLC*"', type=str
)
def validate(*, directory, keep_going, include, exclude, quiet):
    """Check for syntax errors in mods directory"""
    if not quiet:
        click.echo(f"Scanning from directory: {PurePath(directory)}")

    count = 0
    for path in glob.glob("**/*.zdata", root_dir=directory):
        if include and not PurePath(path).match(include):
            continue
        if exclude and PurePath(path).match(exclude):
            continue

        full_path = os.path.join(directory, path)
        if not quiet:
            click.echo(f"Validating {PurePath(full_path)}")

        output = parse_zdata_file(full_path)

        if output.num_errors > 0 and not keep_going:
            sys.exit(1)

        count += 1

    if not quiet:
        click.echo(f"Validated {count} files")


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


if __name__ == "__main__":
    cli()
