#!/usr/bin/env python3

import sqlite3
import sys
import os
from datetime import datetime

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import seo_frontmatter  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netnewswire_db  # noqa: E402

NNW_SEO_PADDING = ("A monthly digest of the best links from the feeds I "
                   "follow. Collected from my favourites in NetNewsWire. "
                   "Subscribe via RSS to get the next one.")

DB_PATH = netnewswire_db.db_path()

# Output path for the generated markdown file
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_PATH = os.path.join(PROJECT_ROOT, '_drafts')

today_str = datetime.now().strftime('%Y-%m-%d')
OUTPUT_FILE = os.path.join(OUT_PATH, f'{today_str}-rss-favourites-digest.md')


def main():
    if not DB_PATH or not os.path.exists(DB_PATH):
        print(
            f"Error: NetNewsWire database not found in iCloud or local path.")
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            items = netnewswire_db.starred(conn)
        except sqlite3.OperationalError as e:
            print(
                f"SQL error: {e}\nCheck table/column names in your NetNewsWire database."
            )
            conn.close()
            return
        if not items:
            print("No favourited articles found.")
        from urllib.parse import urlparse
        from collections import defaultdict

        # Group articles by top-level domain
        domain_groups = defaultdict(list)
        for item in items:
            safe_title = item["title"] if item["title"] else "(No Title)"
            safe_url = item["url"] if item["url"] else None
            if safe_url:
                parsed = urlparse(safe_url)
                domain = parsed.hostname or "other"
                # Only use the top-level domain (e.g. example.com)
                parts = domain.split('.') if domain != "other" else []
                if len(parts) >= 2:
                    tld = '.'.join(parts[-2:])
                else:
                    tld = domain
                domain_groups[tld].append((safe_title, safe_url))

        from datetime import datetime
        now = datetime.now()
        month_year = now.strftime('%B %Y')
        seo_title = seo_frontmatter.fit_title(
            f"RSS Favourites Digest - {month_year}")
        seo_description = seo_frontmatter.fit_description(
            f"My favourite articles saved in my RSS reader in {month_year}, "
            "grouped by website.", NNW_SEO_PADDING)
        frontmatter = ('---\n'
                       f'title: "RSS Favourites Digest: {month_year}"\n'
                       f'seo_title: {seo_frontmatter.quote(seo_title)}\n'
                       'seo_description: '
                       f'{seo_frontmatter.quote(seo_description)}\n'
                       f"date: {now.strftime('%Y-%m-%d')}\n"
                       'layout: post\n'
                       'tags: [digest]\n'
                       '---\n\n')
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            for tld in sorted(domain_groups.keys()):
                f.write(f'## {tld}\n\n')
                for safe_title, safe_url in domain_groups[tld]:
                    f.write(f'- [{safe_title}]({safe_url})\n')
                f.write('\n')
        print(
            f"Exported {sum(len(v) for v in domain_groups.values())} favourited articles to {OUTPUT_FILE}"
        )
        conn.close()
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
