import feedparser
import pathlib
import re
import helper

# Step 1: Define feeds with labels
FEEDS = [("https://www.ft.com/?format=rss", "FT"),
         ("https://www.euronews.com/rss?", "Euronews"),
         ("https://www.theregister.com/headlines.atom", "Register"),
         ("https://weaintgotnohistory.sbnation.com/rss/current.xml", "WAGNH"),
         ("http://developer.apple.com/news/rss/news.rss", "Apple"),
         ("https://cfcnews.thechels.uk/feed.xml", "CFC")]

TIME_DELTA_DAYS = 1

# A bare URL in a headline fails markdownlint (MD034), so it's wrapped in <>.
BARE_URL = re.compile(r"(?<![<(])(https?://[^\s<>]*[^\s<>.,;:!?)\]])")


def news_line(item):
    """One headline as a Markdown list item: title, source and age linked."""
    title = BARE_URL.sub(r"<\1>", item['title'].replace('|', ''))
    icon = item.get("icon", "")
    return f"- {title} ({icon}, [{item['published']}]({item['link']}))\n"


if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        all_items = []

        # Step 2: Add icon to each item
        for url, icon in FEEDS:
            feed = feedparser.parse(url)
            for item in feed["items"][:10]:
                item["icon"] = icon
                all_items.append(item)

        all_items.sort(key=lambda x: x["published_parsed"], reverse=True)

        for item in all_items:
            item["published"] = helper.time_ago(item["published_parsed"])

        cutoff_date = helper.datetime.now() - helper.timedelta(
            days=TIME_DELTA_DAYS)
        all_items = [
            item for item in all_items
            if helper.datetime(*item["published_parsed"][:6]) > cutoff_date
        ]

        string = "".join(news_line(item) for item in all_items)

        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "news_marker", string)
        f.open("w").write(c)
        print("News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
