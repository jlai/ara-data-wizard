import numbers
import re
from collections import namedtuple

MODIFIER = re.compile(r"(?P<operation>[A-Za-z]+)\((?P<values>[^)]+?)\)")

ModifierAction = namedtuple("Modifier", ["operation", "values"])


def parse_number(s: str):
    """Try to parse a number otherwise return str"""

    s = s.strip()
    try:
        return float(s)
    except:
        return s


def parse_modifier_actions(s: str):
    """
    Parse a modifier like:

    ModAdd(Aesthetics, 15.00) and ModAdd(Wealth, 15.00) and ModAdd(Education, 15.00) and ModAdd(Health, 15.00) and ModAdd(Happiness, 15.00)
    """

    return [
        ModifierAction(
            match.group("operation"),
            [parse_number(value) for value in match.group("values").split(",")],
        )
        for match in MODIFIER.finditer(s)
    ]


def get_modifier_text_params(s: str):
    actions = parse_modifier_actions(s)
    params = {}

    for i, action in enumerate(actions):
        first_numeric_value = next(
            (value for value in action.values if isinstance(value, numbers.Number)),
            None,
        )

        if first_numeric_value is not None:
            if action.operation in ["ModMul", "ModMulPerRegionStat"]:
                value = first_numeric_value * 100
            else:
                value = first_numeric_value

            params[f"{i}_value"] = f"{value:+10g}".strip()

    return params
