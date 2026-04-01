import html
import pathlib
import time
from urllib.parse import parse_qs, urlparse
import feedparser
import helper

SOURCE = "https://www.youtube.com/feeds/videos.xml?channel_id=UCwK4oZ8hw9RS6tZKEjw_qLw"

def get_embed_url(link: str) -> str:
    parsed = urlparse(link)

    if parsed.netloc in {"www.youtube.com", "youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
        else:
            video_id = ""
    elif parsed.netloc == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/", 1)[0]
    else:
        video_id = ""

    if not video_id:
        raise ValueError(f"Unable to extract YouTube video ID from {link}")

    return f"https://www.youtube.com/embed/{video_id}"


if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        all_items = []

        feed = feedparser.parse(SOURCE)
        for item in feed["items"]:
            all_items.append(item)

        all_items.sort(key=lambda x: x["published_parsed"], reverse=True)

        string = ""
        for item in all_items:
            title = item["title"].replace("|", "").strip()
            embed_url = get_embed_url(item["link"])
            escaped_title = html.escape(title, quote=True)
            published = time.strftime("%Y-%m-%d", item["published_parsed"])
            string += (
                "<div class=\"posts\">\n"
                f"  <h2>{title}</h2>\n"
                f"  <span class=\"meta\">{published}</span>\n"
                f"  <iframe width=\"100%\" height=\"315\" src=\"{embed_url}\" title=\"{escaped_title}\" "
                "loading=\"lazy\" referrerpolicy=\"strict-origin-when-cross-origin\" "
                "allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" allowfullscreen></iframe>\n"
                "</div>\n\n"
            )

        f = root / "_layouts/videos.html"
        m = f.open().read()
        c = helper.replace_chunk(m, "videos_marker", string)
        f.open("w").write(c)
        print("Videos completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")