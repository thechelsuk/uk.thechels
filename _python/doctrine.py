import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OUTPUT_FILE = root / "_pages/daily.md"
    INPUT_FILE = "./_data/doctrine.yml"
    KEY = "doctrine_marker"
    string = helper.FileProcessorPicksRandomItem(OUTPUT_FILE=OUTPUT_FILE, INPUT_SOURCE=INPUT_FILE, KEY=KEY)
    print(string)
