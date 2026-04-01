import html
import pathlib
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import helper

SOURCE = "https://www.youtube.com/feeds/videos.xml?channel_id=UCwK4oZ8hw9RS6tZKEjw_qLw"
NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
}


def get_text(element: ET.Element, path: str) -> str:
    value = element.findtext(path, default="", namespaces=NAMESPACES)
    return value.strip()


def get_alternate_link(entry: ET.Element) -> str:
    for link in entry.findall("atom:link", NAMESPACES):
        if link.get("rel") == "alternate":
            return link.get("href", "")
    return ""


def get_videos() -> list[dict[str, str | None]]:
    with urlopen(SOURCE) as response:
        root = ET.fromstring(response.read())

    videos = []
    for entry in root.findall("atom:entry", NAMESPACES):
        star_rating = entry.find(
            "media:group/media:community/media:starRating", NAMESPACES)
        statistics = entry.find("media:group/media:community/media:statistics",
                                NAMESPACES)
        videos.append({
            "title":
            get_text(entry, "atom:title").replace("|", "").strip(),
            "link":
            get_alternate_link(entry),
            "published":
            get_text(entry, "atom:published")[:10],
            "rating_average":
            star_rating.get("average") if star_rating is not None else None,
            "rating_count":
            star_rating.get("count") if star_rating is not None else None,
            "views":
            statistics.get("views") if statistics is not None else None,
        })

    videos.sort(key=lambda item: item["published"] or "", reverse=True)
    return videos


def format_meta(video: dict[str, str | None]) -> str:
    meta = [video["published"] or ""]

    if video["views"]:
        meta.append(f"{int(video['views']):,} views")

    if video["rating_average"] and video["rating_count"]:
        rating_count = int(video["rating_count"])
        rating_label = "rating" if rating_count == 1 else "ratings"
        meta.append(
            f"{video['rating_average']}/5 from {rating_count:,} {rating_label}"
        )

    return " // ".join(part for part in meta if part)


if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        all_items = get_videos()

        string = ""
        for item in all_items:
            title = item["title"] or ""
            video_link = item["link"] or ""
            escaped_title = html.escape(title, quote=True)
            escaped_link = html.escape(video_link, quote=True)
            meta = html.escape(format_meta(item), quote=False)
            string += (
                "<div class=\"posts\">\n"
                f"  <h2>{escaped_title}</h2>\n"
                f"  <span class=\"meta\">{meta}</span>\n"
                "  <ul>\n"
                f"    <li><a href=\"{escaped_link}\">Watch on YouTube</a></li>\n"
                "  </ul>\n"
                "</div>\n\n")

        f = root / "_layouts/videos.html"
        m = f.open().read()
        c = helper.replace_chunk(m, "videos_marker", string)
        f.open("w").write(c)
        print("Videos completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
