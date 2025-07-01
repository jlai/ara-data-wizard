import json
import click

from cli.base import cli, load_database
from exporters.json import ExportJsonOptions, make_serialize, transform
from game_data.database import GameDatabase
from pprint import pp


@cli.group()
def query():
    pass


@query.command()
@load_database
@click.argument("key")
@click.option("--count", default=1)
def text(key, *, db: GameDatabase, count):
    """Get the text for a text key"""
    text = db.get_text(key, count=count)
    print(text)


@query.command()
@load_database
@click.argument("id")
@click.option("--format", type=click.Choice(["json", "pp"]), default="pp")
def object(id, *, db: GameDatabase, format):
    """Get an object by id"""
    objs = list(db.all_objects.where(id=id))

    if len(objs) == 1:
        objs = objs[0]

    options = ExportJsonOptions()

    match format:
        case "pp":
            pp(vars(objs))
        case "json":
            print(
                json.dumps(
                    transform(objs, pre_func=make_serialize(options, db=db)), indent=4
                )
            )
