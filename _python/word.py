# importing modules
import pathlib
import feedparser
import helper

root = pathlib.Path(__file__).parent.parent.resolve()
item = feedparser.parse("https://wordsmith.org/awad/rss1.xml")['entries']
title = item[0]["title"]
desc = item[0]["summary"]
string = f"\n > {title} - {desc}\n"

if __name__ == "__main__":
    mdFile = root / "_pages/morning.md"
    mdFile_contents = mdFile.open().read()
    rewritten = helper.replace_chunk(mdFile_contents, "word_marker", string)
    mdFile.open("w").write(rewritten)
    print("Word completed")
