import os
import sqlite3
import sys

LOCAL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "local"))
if LOCAL_DIR not in sys.path:
    sys.path.insert(0, LOCAL_DIR)

import netnewswire_db  # noqa: E402


def make_db(path):
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE articles (
            articleID TEXT, feedID TEXT, title TEXT, contentHTML TEXT,
            contentText TEXT, url TEXT, externalURL TEXT, summary TEXT,
            datePublished REAL);
        CREATE TABLE statuses (articleID TEXT, read INTEGER, starred INTEGER);
    """)
    conn.executemany("INSERT INTO articles VALUES (?,?,?,?,?,?,?,?,?)", [
        ("a1", "https://feed.one/rss", "Older", "<p>One</p>", None,
         "https://feed.one/older", None, "s1", 1700000000.0),
        ("a2", "https://feed.two/rss", None, None, "Two", None,
         "https://elsewhere.example/two", None, 1750000000.0),
        ("a3", "https://feed.one/rss", "Not starred", None, None,
         "https://feed.one/x", None, None, 1760000000.0),
    ])
    conn.executemany("INSERT INTO statuses VALUES (?,?,?)", [("a1", 1, 1),
                                                             ("a2", 0, 1),
                                                             ("a3", 0, 0)])
    conn.commit()
    return conn


def test_db_path_returns_first_existing(tmp_path):
    missing = tmp_path / "missing.sqlite3"
    present = tmp_path / "DB.sqlite3"
    present.write_bytes(b"")
    assert netnewswire_db.db_path([str(missing), str(present)]) == str(present)


def test_db_path_none_when_nothing_exists(tmp_path):
    assert netnewswire_db.db_path([str(tmp_path / "nope")]) is None


def test_starred_returns_only_starred_newest_first(tmp_path):
    conn = make_db(tmp_path / "DB.sqlite3")
    items = netnewswire_db.starred(conn)
    assert [i["article_id"] for i in items] == ["a2", "a1"]


def test_starred_prefers_external_url_and_fills_fields(tmp_path):
    conn = make_db(tmp_path / "DB.sqlite3")
    newest, older = netnewswire_db.starred(conn)
    assert newest["url"] == "https://elsewhere.example/two"
    assert newest["title"] is None
    assert newest["content_text"] == "Two"
    assert older["url"] == "https://feed.one/older"
    assert older["feed_id"] == "https://feed.one/rss"
    assert older["content_html"] == "<p>One</p>"
    assert older["summary"] == "s1"
    assert older["date_published"] == "2023-11-14"
