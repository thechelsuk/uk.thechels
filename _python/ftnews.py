# importing modules
import pathlib

import feedparser
import helper

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        nf = feedparser.parse("https://www.ft.com/?format=rss")["entries"]
        nh = "\n".join([f" - {entry['title']}" for entry in nf[5]])
        string = f"\n{nh}\n"
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "ftnews_marker", string)
        f.open("w").write(c)
        print("news completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
