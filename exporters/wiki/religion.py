import textwrap
from exporters.wiki.base import (
    WikiPageUpdater,
)


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

        for verse in self.db.all_objects.by._type["ReligionBuffTemplate"]:
            # FIXME currently not included
            if verse.id == "vrs_Culture6":
                continue

            code += "|-\n"
            code += "| " + self.get_domain_link(verse.Domain) + "\n"
            code += "| " + self.db.get_text(verse.Name) + "\n"
            code += "| " + self.describe_buff(verse.Buff) + "\n"

        code += "|}"

        code = f"<!-- ara-data-wizard: BEGIN GENERATED CONTENT -->\n{code}\n<!-- ara-data-wizard: END GENERATED CONTENT -->"

        self.write_code(code, output_filename=output_filename)
