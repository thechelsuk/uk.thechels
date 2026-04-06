#!/usr/bin/env python3
"""
fetch_social.py
Fetches Bluesky and Mastodon RSS feeds, merges into _data/*.yml
Only posts tagged #firehose are saved. Posts linking to thechels.uk are excluded.
Existing entries are preserved; only new ones are appended (RSS limit ~10-20 posts).
"""

import re
import feedparser
import yaml
from calendar import timegm
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
BLUESKY_RSS    = "https://bsky.app/profile/did:plc:dz7xwi7wgfyzk4oemurkomax/rss"
MASTODON_RSS   = "https://mastodon.social/@Thechelsuk.rss"
DATA_DIR       = Path("_data")
FIREHOSE_TAG   = "#firehose"
EXCLUDE_DOMAIN = "thechels.uk"

# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()

def _str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if "'" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)

yaml.add_representer(str, _str_representer)

def load_yaml(path: Path) -> list:
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f) or []
    return []

def save_yaml(path: Path, data: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"  Saved {len(data)} entries -> {path}")

def merge_entries(existing: list, new_entries: list, id_key: str = "id") -> tuple[list, int]:
    seen = {str(e[id_key]) for e in existing if id_key in e}
    added = 0
    for entry in new_entries:
        eid = str(entry.get(id_key, ""))
        if eid and eid not in seen:
            existing.append(entry)
            seen.add(eid)
            added += 1
    existing.sort(key=lambda x: x.get("date", ""), reverse=True)
    return existing, added

def parse_feed(url: str, label: str) -> list:
    print(f"  Fetching {label} RSS from {url}...")
    feed = feedparser.parse(url)
    if feed.bozo and not feed.entries:
        print(f"  WARNING: {label} feed parse error: {feed.bozo_exception}")
        return []

    entries = []
    for entry in feed.entries:
        link = entry.get("link", "")
        raw_summary = entry.get("summary", entry.get("description", ""))
        text = strip_html(raw_summary)

        # Only include posts tagged #firehose
        if FIREHOSE_TAG.lower() not in text.lower():
            continue

        # Exclude posts linking back to the site
        if EXCLUDE_DOMAIN in text or EXCLUDE_DOMAIN in link:
            continue

        if entry.get("published_parsed"):
            dt = datetime.fromtimestamp(timegm(entry.published_parsed), tz=timezone.utc)
        else:
            dt = datetime.now(timezone.utc)

        entries.append({
            "id":      entry.get("id", link),
            "title":   f"{label} post on {dt.strftime('%Y-%m-%d')}",
            "link":    link,
            "date":    dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "summary": text,
            "type":    "note",
        })

    print(f"  Found {len(entries)} {label} posts tagged {FIREHOSE_TAG}")
    return entries

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    bluesky_path = DATA_DIR / "bluesky.yml"
    existing_bs  = load_yaml(bluesky_path)
    new_bs       = parse_feed(BLUESKY_RSS, "Bluesky")
    merged_bs, added_bs = merge_entries(existing_bs, new_bs)
    print(f"  Bluesky: +{added_bs} new entries")
    save_yaml(bluesky_path, merged_bs)

    mastodon_path = DATA_DIR / "mastodon.yml"
    existing_md   = load_yaml(mastodon_path)
    new_md        = parse_feed(MASTODON_RSS, "Mastodon")
    merged_md, added_md = merge_entries(existing_md, new_md)
    print(f"  Mastodon: +{added_md} new entries")
    save_yaml(mastodon_path, merged_md)

if __name__ == "__main__":
    main()
