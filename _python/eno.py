# importing modules
import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OUTPUT_FILE = root / "_pages/daily.md"
    URL = "https://jamesg.blog/oblique-strategies/rss.xml"
    KEY = "eno_marker"
    string = helper.FeedProcessor(OUTPUT_FILE, URL, KEY)
    print(string)

