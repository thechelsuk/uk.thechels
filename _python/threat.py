from datetime import datetime
import feedparser
import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OUTPUT_FILE = root / "_pages/daily.md"
    nf = feedparser.parse(
        "https://www.mi5.gov.uk/UKThreatLevel/UKThreatLevel.xml")["entries"]
    if nf:
        entry = nf[0]
        last_word = entry['title'].split()[-1]
        update_dt = datetime.strptime(entry['published'],
                                      "%A, %B %d, %Y -  %H:%M")
        days_since_update = (datetime.now() - update_dt).days
        update = update_dt.strftime("%Y-%m-%d")
        string = f'- The current threat level is <span class="highlighter">{last_word}</span>\n'
        string += f"- It has been {days_since_update} days since the last change ({update})\n"
    else:
        string = '- Unable to fetch threat level data.\n'
        days_since_update = 0
        update = ''
    KEY = "threat_marker"
    string = helper.FileProcessorFromSource(OUTPUT_FILE, string, KEY)
    print(string)
