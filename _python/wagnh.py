import feedparser
import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OUTPUT_FILE = root / "_pages/daily.md"
    nf = feedparser.parse(
        "https://weaintgotnohistory.sbnation.com/rss/current.xml")["entries"]
    nh = "\n".join([f"- {entry['title']}" for entry in nf[:10]])
    string = f"\n{nh}\n"
    KEY = "news_marker"
    string = helper.FileProcessorFromSource(OUTPUT_FILE, string, KEY)
    print(string)
