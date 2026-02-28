import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OF = root / "_pages/daily.md"
    IF = "./_data/blogroll.yml"
    KEY = "blogroll_marker"
    string = helper.FileProcessorPicksRandomObjects(OF=OF, IF=IF, KEY=KEY, count=3)
    print(string)