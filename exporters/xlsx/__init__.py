import xlsxwriter

from game_data.database import GameDatabase

from .improvements_sheet import ImprovementsSheetGenerator
from .items_sheet import ItemsSheetGenerator


def generate_xlsx(filename: str, db: GameDatabase):
    with xlsxwriter.Workbook(filename) as workbook:
        ImprovementsSheetGenerator(
            db, workbook, workbook.add_worksheet("Improvements")
        ).create()
        ItemsSheetGenerator(db, workbook, workbook.add_worksheet("Items")).create()
