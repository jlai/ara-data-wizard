from antlr4 import InputStream
from game_data.zdata.parse import parse_zdata_stream


def test_simple():
    FILE = """
    schema Test;

    export SomeData some_data = {
        .Name = "Some name",
    };
    """

    zdata = parse_zdata_stream(InputStream(FILE))
    assert zdata.exports["some_data"]["Name"] == "Some name"


def test_union():
    FILE = """
    schema Test;

    export SomeData some_data = {
        .Name = "Some name",
        .Flags = (Flags.A | Flags.B),
    };
    """

    zdata = parse_zdata_stream(InputStream(FILE))
    assert zdata.exports["some_data"]["Flags"] == ["Flags.A", "Flags.B"]


def test_variables():
    FILE = """
    schema Test;

    int FutureCost = 1000;

    export SomeData some_data = {
        .Name = "Some name",
        .Cost = FutureCost + 500,
    };
    """

    zdata = parse_zdata_stream(InputStream(FILE))
    assert zdata.exports["some_data"]["Cost"] == 1500
