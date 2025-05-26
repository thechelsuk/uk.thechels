from ast import Is
import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OF = root / "_pages/daily.md"
    IF = "./_data/doctrine.yml"
    KEY = "doctrine_marker"
    string = helper.FileProcessorPicksRandomItem(OF=OF,IF=IF,KEY=KEY)
    print(string)
