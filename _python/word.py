# importing modules
import pathlib
from platform import mac_ver
import feedparser
import helper

root = pathlib.Path(__file__).parent.parent.resolve()
item = feedparser.parse("https://wordsmith.org/awad/rss1.xml")['entries']
title = item[0]["title"]
desc = item[0]["summary"]
string = f"\n > {title} - {desc}\n"

if __name__ == "__main__":
    f = root / "_pages/morning.md"
    m = f.open().read()
    r = helper.replace_chunk(m, "word_marker", string)
    m.open("w").write(r)
    print("Word completed")
