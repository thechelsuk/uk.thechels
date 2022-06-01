"""
Get RSS feed
"""
import re
import pathlib
import feedparser

root = pathlib.Path(__file__).parent.parent.resolve()

def replace_chunk(content, marker, chunk):
    """ Swap out placeholders """
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

item = feedparser.parse("https://wordsmith.org/awad/rss1.xml")['entries']
title = item[0]["title"]
desc = item[0]["summary"]
string = f"\n > {title} - {desc} \n"

print(string)

if __name__ == "__main__":
    readme = root / "_pages/morning.md"
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "word_marker", string)
    readme.open("w").write(rewritten)

    print("Word completed")
