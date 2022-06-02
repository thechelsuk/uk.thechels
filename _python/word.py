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

# processing
if __name__ == "__main__":
    try:
        f = root / "_pages/morning.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "word_marker", string)
        f.open("w").write(c)
        print("Word completed")
    except FileNotFoundError:
        print('File does not exist, unable to proceed')