import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OUTPUT_FILE = root / "_pages/daily.md"
    SOURCE = "https://www.live-footballontv.com/live-english-football-on-tv.html"
    data = helper.get_fixtures(SOURCE)
    KEY = "fixture_marker"
    string = helper.FileProcessorFromSource(OUTPUT_FILE, data, KEY)
    print(string)
