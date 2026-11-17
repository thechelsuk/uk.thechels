import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import news


def item(title):
    return {
        "title": title,
        "icon": "CFC",
        "published": "2 hours ago",
        "link": "https://example.com/a"
    }


def test_plain_title():
    assert news.news_line(item("Chelsea win")) == \
        "- Chelsea win (CFC, [2 hours ago](https://example.com/a))\n"


def test_bare_url_in_title_is_wrapped():
    # markdownlint MD034 fails a bare URL
    line = news.news_line(
        item("Moved: subscribe to https://cfcnews.thechels.uk/feed.xml"))
    assert "subscribe to <https://cfcnews.thechels.uk/feed.xml> (CFC" in line


def test_pipes_removed():
    assert news.news_line(item("A | B"))[:7] == "- A  B "
