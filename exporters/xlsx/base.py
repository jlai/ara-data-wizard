from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from game_data.database import GameDatabase
from game_data.modifiers import get_modifier_text_params


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

        self.merge_format = self.workbook.add_format(
            {
                "bold": True,
                "border": 6,
                "align": "left",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )

    def write_row(self, columns):
        for i, column in enumerate(columns):
            self.sheet.write(self.next_row, i, column)
        self.next_row += 1

    def get_text(self, key, *, count=1, params={}):
        return self.db.get_text(key, count=count, params=params)

    def write_section_header(self, text: str):
        self.sheet.merge_range(
            self.next_row,
            0,
            self.next_row,
            self.sheet.dim_colmax,
            text,
            self.merge_format,
        )
        self.sheet.set_row(self.next_row, height=32)
        self.next_row += 1

    def setup_header(self, column_templates: list[ColumnTemplate]):
        last_column = len(column_templates)

        # Hide rows and columns outside range
        self.sheet.set_column(
            last_column, self.sheet.xls_colmax - 1, None, None, {"hidden": True}
        )
        self.sheet.set_default_row(hide_unused_rows=True)

        # Write header
        self.write_row([column_template.name for column_template in column_templates])
        self.sheet.set_row(0, 48)

        for c, column_template in enumerate(column_templates):
            column_format = self.workbook.add_format(
                {"align": column_template.align, "valign": "vcenter", "text_wrap": True}
            )
            self.sheet.set_column(c, c, None, column_format)

        # Hide rows and columns outside range
        self.sheet.set_column(
            last_column, self.sheet.xls_colmax - 1, None, None, {"hidden": True}
        )

    def finish(self):
        self.sheet.autofit(300)
        self.sheet.freeze_panes(1, 1)

    def describe_buffs(self, buff_ids):
        descs = []
        for buff_id in buff_ids:
            if not buff_id:
                continue

            buff = self.db.buffs.by.id[buff_id]
            params = get_modifier_text_params(buff.modifiers)
            descs.append(self.get_text(buff.description, params=params))
        return descs
