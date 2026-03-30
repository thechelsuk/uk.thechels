import feedparser
import pathlib
import helper

URL_1 = "feed_url_here"

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OF = root / "_pages/daily.md"
    nf = feedparser.parse(
        URL_1)["entries"]
    nh = "\n".join([f"- {entry['title']}" for entry in nf[:10]])
    string = f"\n{nh}\n"
    KEY = "news_marker"
    string = helper.FileProcessorFromSource(OF, string, KEY)
    print(string)
