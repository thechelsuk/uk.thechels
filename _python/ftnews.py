# importing modules
import pathlib

import feedparser
import helper

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        news_feed = feedparser.parse(
            "https://www.ft.com/?format=rss"
        )["entries"]
        news_headlines = "\n".join(
            [f" - {entry['title']}" for entry in news_feed[:8]])
        string = f"\n{news_headlines}\n"
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "ftnews_marker", string)
        f.open("w").write(c)
        print("news completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
