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
    items = feedparser.parse("https://wordsmith.org/awad/rss1.xml")["item"]
    return [
        {
            "title": item["title"],
            "desc": item["description"]
        }
        for item in items
    ]

if __name__ == "__main__":
    readme = root / "morning.html"
    readme_contents = readme.open().read()
    item = fetch_blog_entries()[:1]
    word = "\n ###" + item[title] + "\n > " + item[desc] + "\n"
    rewritten = replace_chunk(readme_contents, "word", word)
    readme.open("w").write(rewritten)
