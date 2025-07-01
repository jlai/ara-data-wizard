import glob
import sys
import click
import os

from pathlib import PurePath
from game_data.zdata.parse import parse_zdata_file
from cli.base import cli
from cli.config import config


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
