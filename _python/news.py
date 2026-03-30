import feedparser
import pathlib
import helper

# Step 1: Define feeds with icons
FEEDS = [
    ("https://www.ft.com/?format=rss", "£"),
    ("https://www.euronews.com/rss?", "€"),
    ("https://www.theregister.com/headlines.atom", "®"),
    ("https://weaintgotnohistory.sbnation.com/rss/current.xml", "♣")
]

TIME_DELTA_DAYS = 2

if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        all_items = []

        # Step 2: Add icon to each item
        for url, icon in FEEDS:
            feed = feedparser.parse(url)
            for item in feed["items"][:25]:
                item["icon"] = icon
                all_items.append(item)

        all_items.sort(key=lambda x: x["published_parsed"], reverse=True)

        for item in all_items:
            item["published"] = helper.time_ago(item["published_parsed"])

        cutoff_date = helper.datetime.now() - helper.timedelta(days=TIME_DELTA_DAYS)
        all_items = [item for item in all_items if helper.datetime(*item["published_parsed"][:6]) > cutoff_date]

        string = ""
        for item in all_items:
            title = item['title'].replace('|', '')
            icon = item.get("icon", "")
            string += f"- {icon} {title} ([{item['published']}]({item['link']}))\n"

        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "news_marker", string)
        f.open("w").write(c)
        print("News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")