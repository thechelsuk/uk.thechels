# importing modules
import pathlib

import feedparser
import helper
from datetime import datetime

URL = "https://www.mi5.gov.uk/UKThreatLevel/UKThreatLevel.xml"

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        output = feedparser.parse(URL)["entries"]

        for entry in output:
            level = (f"{entry['title']}")
            last_word = level.split()[-1]
            update = entry['published']
            update = datetime.strptime(
                update, "%A, %B %d, %Y -  %H:%M").strftime("%Y-%m-%d")
            days_since_update = (datetime.now() -
                                 datetime.strptime(update, "%Y-%m-%d")).days

        string = f'- The current threat level is <span class="highlighter">{last_word}</span>\n'
        string += f"- It has been {days_since_update} days since the last change ({update})\n"
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "threat_marker", string)
        f.open("w").write(c)
        print("threat completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
