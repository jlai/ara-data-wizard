import click

from cli.base import cli, load_database
from exporters.wiki.goods import GoodsPageUpdater


@cli.group("wiki")
def wiki():
    pass


@wiki.command()
@load_database
@click.argument("page")
@click.option("-o", "output_filename", help="Output filename", default="-")
def update(*, page, db, output_filename):
    """Output an updated version of an existing wiki page. Changes must be manually applied."""

    match page:
        case "goods":
            updater = GoodsPageUpdater(db)
            updater.update_page(output_filename=output_filename)
        case _:
            print(f"Unknown page {page}")
