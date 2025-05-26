import feedparser
import pathlib
import helper

if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.resolve()
    OF = root / "_pages/daily.md"
    nf = feedparser.parse("https://wordsmith.org/awad/rss1.xml")["entries"]
    title = nf[0]["title"]
    desc = nf[0]["summary"]
    string = f"\n > {title} - {desc}\n"
    KEY = "word_marker"
    string = helper.FileProcessorFromSource(OF, string, KEY)
    print(string)
