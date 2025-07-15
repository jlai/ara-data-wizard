import textwrap
from exporters.wiki.base import (
    WikiPageUpdater,
)
from game_data.objects import ReligiousVerse


class ReligiousVersesUpdater(WikiPageUpdater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, *, output_filename):
        code = ""

        code = textwrap.dedent(
            r"""
        {{#css:
        .wikitable.center-first td:first-child {
            text-align: center;
        }
        }}
        {|class="wikitable"
        ! Domain
        ! Name
        ! Benefit
        """
        )

        for verse in self.db.get_object_table("ReligionBuffs", ReligiousVerse):
            code += "|-\n"
            code += "| " + self.get_domain_link(verse.domain) + "\n"
            code += "| " + verse.get_name() + "\n"
            code += "| " + self.describe_buff(verse.buff) + "\n"

        code += "|}"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)
