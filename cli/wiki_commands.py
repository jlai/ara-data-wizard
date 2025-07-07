import click

from cli.base import cli, load_database
from exporters.wiki.goods import GoodsPageUpdater
from exporters.wiki.religion import ReligiousVersesUpdater
from exporters.wiki.techs import TechsPageUpdater
from exporters.wiki.units import UnitsPageUpdater


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


@wiki.command()
@load_database
@click.argument("page")
@click.option("-o", "output_filename", help="Output filename", default="-")
def generate(*, page, db, output_filename):
    """Output an updated version of an existing wiki page. Changes must be manually applied."""

    match page:
        case "techs":
            updater = TechsPageUpdater(db)
            updater.write_techs(output_filename=output_filename)
        case "units":
            updater = UnitsPageUpdater(db)
            updater.write_units(output_filename=output_filename)
        case "harvested-goods":
            updater = GoodsPageUpdater(db)
            updater.generate_harvested_goods_code(output_filename=output_filename)
        case "verses":
            updater = ReligiousVersesUpdater(db)
            updater.write(output_filename=output_filename)
        case _:
            print(f"Unknown page {page}")
