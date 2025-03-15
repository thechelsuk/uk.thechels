# importing modules
import pathlib

import feedparser
import helper
from datetime import datetime

URL = "https://jamesg.blog/oblique-strategies/rss.xml"

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        output = feedparser.parse(URL)["entries"]

        for entry in output:
            out_string = entry['title']

        string = f'> {out_string}\n'
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "eno_marker", string)
        f.open("w").write(c)
        print("Oblique Strategies completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
