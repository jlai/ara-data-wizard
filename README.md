# Data Wizard for Ara: History Untold

A tool for dealing with data from [Ara: History Untold](https://www.arahistoryuntold.com/).
This is an unofficial third-party tool and is not affiliated with the developers of Ara.

## Setup

This assumes you have some basic familiarity with the command line and Python.

```bash
pip install -r requirements.txt
```

## Configuring the game assets directory

Create a `.AraWizard.toml` file in this source directory or in your home directory (in `%USERPROFILE%` on Windows) with
the path to the game assets directory. Note that it's asset**s**-dir not asset-dir.

```toml
assets-dir = 'C:\Program Files (x86)\Steam\steamapps\common\Ara History Untold\assets'
mods-dir = 'C:\Users\YourNameHere\Documents\My Games\Ara History Untold\Mods'
```

Alternatively, you can pass it via `--assets-dir=` on the command line.

## Generating a spreadsheet

To generate an Excel (.xlsx) spreadsheet:

```bash
python wizard.py excel -o "out/Ara Game Data.xlsx"
```

## Visualizing goods with Graphviz

You can output a dependency graph of the goods crafting in the game. Sample output [here](docs/Ara%20Goods%201.4.pdf).

```bash
python wizard.py graphviz -o "out/Ara Goods.pdf"
```

## Exporting to JSON

To dump a .json file:

```bash
python wizard.py json -o out/ara.json
```

You can then query the file with a tool like [jq](https://jqlang.org/tutorial/).

## Extracting images

You can extract individual images from image atlases by pointing at the .xml file
(relative to the assets directory):

```
python wizard.py images -o "out/images" UI/Art/Icons/Improvements_256.xml
```

## Validating mod files

To check for syntax errors (such as missing commas) in your mod files, you can run.

```bash
python wizard.py validate
```

To check a subset of files in the Mods directory, you can filter using a wildcard pattern:

```bash
python wizard.py validate --include DefaultMod/*
python wizard.py validate --include Improvements*.zdata
```

Use `--help` to see more options. Note that currently this only checks the syntax and not
the schema / data types of your objects.

## Troubleshooting

### Clearing the cache

If you've updated the source code or are having trouble, delete the `.cache` directory
to clear out cached data.
