from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from game_data.database import GameDatabase


class ColumnTemplate:
    def __init__(self, name: str, align="center"):
        self.name = name
        self.align = align


class SheetGenerator:
    def __init__(self, db: GameDatabase, workbook: Workbook, sheet: Worksheet):
        self.db = db
        self.workbook = workbook
        self.sheet = sheet
        self.next_row = 0

    def write_row(self, columns):
        for i, column in enumerate(columns):
            self.sheet.write(self.next_row, i, column)
        self.next_row += 1

    def get_text(self, key, *, count=1, params={}):
        return self.db.get_text(key, count=count, params=params)

    def setup_header(self, column_templates: list[ColumnTemplate]):
        last_column = len(column_templates)

        self.write_row([column_template.name for column_template in column_templates])

        for c, column_template in enumerate(column_templates):
            column_format = self.workbook.add_format(
                {"align": column_template.align, "valign": "vcenter", "text_wrap": True}
            )
            self.sheet.set_column(c, c, None, column_format)

        # Hide rows and columns outside range
        self.sheet.set_default_row(hide_unused_rows=True)
        self.sheet.set_column(
            last_column, self.sheet.xls_colmax - 1, None, None, {"hidden": True}
        )

    def finish(self):
        self.sheet.autofit(300)
        self.sheet.freeze_panes(1, 1)
