# Grammar

This contains the [ANTLR](https://www.antlr.org/) grammar files for parsing Oxide Games' zdata
configuration scripting language. The grammar was created by looking through the SourceMods
directory in [Ara: History Untold](https://www.arahistoryuntold.com/) so this is an incomplete
representation of the language.

## Regenerating parser files

Only necessary if you're modifying the grammar files. This regenerates the Python source for
the parser.

```bash
npm install -g antlr-ng
antlr-ng -Dlanguage=Python3 -p generated -l false -v true -o game_data/zdata/generated grammar/ZdataLexer.g4 grammar/ZdataParser.g4
```
