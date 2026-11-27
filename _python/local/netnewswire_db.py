import os
from datetime import datetime, timezone

CANDIDATE_PATHS = [
    os.path.expanduser(
        '~/Library/Containers/com.ranchero.NetNewsWire-Evergreen/Data/Library/Application Support/NetNewsWire/Accounts/2_iCloud/DB.sqlite3'
    ),
    os.path.expanduser(
        '~/Library/Application Support/NetNewsWire/Accounts/OnMyMac/DB.sqlite3'
    ),
]

STARRED_QUERY = """
    SELECT articles.articleID, articles.feedID, articles.title,
           articles.url, articles.externalURL, articles.summary,
           articles.contentHTML, articles.contentText, articles.datePublished
    FROM articles
    INNER JOIN statuses ON statuses.articleID = articles.articleID
    WHERE statuses.starred = 1
    ORDER BY articles.datePublished DESC
"""


def db_path(candidates=None):
    for path in candidates or CANDIDATE_PATHS:
        if os.path.exists(path):
            return path
    return None


def _date(timestamp):
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d')


def starred(conn):
    items = []
    for (article_id, feed_id, title, url, external_url, summary, content_html,
         content_text, date_published) in conn.execute(STARRED_QUERY):
        items.append({
            "article_id": article_id,
            "feed_id": feed_id,
            "title": title,
            "url": external_url or url,
            "summary": summary,
            "content_html": content_html,
            "content_text": content_text,
            "date_published": _date(date_published),
        })
    return items
