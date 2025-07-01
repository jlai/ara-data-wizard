import functools
import os.path
import click

from game_data.database import GameDatabase
from cli.config import config


@click.group()
def cli():
    pass


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
