# importing modules
import feedparser
import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OUTPUT_FILE = root / "_pages/daily.md"
    nf = feedparser.parse("https://www.ft.com/?format=rss")["entries"]
    nh = "\n".join([f"- {entry['title']}" for entry in nf[:8]])
    string = f"\n{nh}\n"
    KEY = "ftnews_marker"
    string = helper.FileProcessorFromSource(OUTPUT_FILE, string, KEY)
    print(string)
