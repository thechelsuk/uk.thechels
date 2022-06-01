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

def fetch_blog_entries():
    entries = feedparser.parse("https://wordsmith.org/awad/rss1.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "desc": entry["description"]
        }
        for entry in entries
    ]

if __name__ == "__main__":
    readme = root / "_pages/morning.md"
    readme_contents = readme.open().read()
    entries = fetch_blog_entries()[:1]
    word = "\n".join("####" + {title} + "\n > " + {desc} + "\n".format(**entry) for entry in entries])
    rewritten = replace_chunk(readme_contents, "word", word)
    readme.open("w").write(rewritten)

    print("Word completed")
