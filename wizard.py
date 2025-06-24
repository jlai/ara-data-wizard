from pathlib import PurePath
import sys
import click
import tomllib
import os.path
import glob
from exporters.json import generate_json
from exporters.xlsx import generate_xlsx
from game_data.database import GameDatabase
from game_data.zdata.parse import parse_zdata_file

config = {}

for config_location in [".AraWizard.toml", os.path.expanduser("~/.AraWizard.toml")]:
    if os.path.exists(config_location):
        with open(config_location, "rb") as f:
            config = tomllib.load(f)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--assets-dir",
    help="Game assets directory path",
    required=True,
    default=config.get("assets-dir"),
)
@click.option(
    "-o", "output_filename", help="Output filename", default="Ara Game Data.xlsx"
)
def excel(assets_dir=None, output_filename=None):
    """Create a XLSX file with various data from the game."""
    db = GameDatabase(assets_dir)
    generate_xlsx(output_filename, db)

    click.echo(f"Spreadsheet written to {output_filename}")


@cli.command()
@click.option(
    "--assets-dir",
    help="Game assets directory path",
    required=True,
    default=config.get("assets-dir"),
)
@click.option("-o", "output_filename", help="Output filename", default="ara-data.json")
def json(assets_dir=None, output_filename=None):
    """Create a JSON file with various data from the game."""
    db = GameDatabase(assets_dir)
    generate_json(output_filename, db)

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
def validate(directory, keep_going=False, include=None, exclude=None, quiet=False):
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


if __name__ == "__main__":
    cli()
