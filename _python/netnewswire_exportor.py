#!/usr/bin/env python3

import sqlite3
import os

# NetNewsWire database path (checks user-provided iCloud path first, then local)
USER_ICLOUD_PATH = os.path.expanduser('~/Library/Containers/com.ranchero.NetNewsWire-Evergreen/Data/Library/Application Support/NetNewsWire/Accounts/2_iCloud/DB.sqlite3')
LOCAL_PATH = os.path.expanduser('~/Library/Application Support/NetNewsWire/Accounts/OnMyMac/DB.sqlite3')

if os.path.exists(USER_ICLOUD_PATH):
    DB_PATH = USER_ICLOUD_PATH
elif os.path.exists(LOCAL_PATH):
    DB_PATH = LOCAL_PATH
else:
    DB_PATH = None


from datetime import datetime
today_str = datetime.now().strftime('%Y-%m-%d')
OUTPUT_FILE = os.path.expanduser(f'~/Desktop/{today_str}-rss-favourites-digest.md')

def main():
    if not DB_PATH or not os.path.exists(DB_PATH):
        print(f"Error: NetNewsWire database not found in iCloud or local path.")
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # Try common table/column names for favourited articles
        query = """
            SELECT articles.title, articles.summary,  articles.url, articles.externalURL
            FROM articles
            INNER JOIN statuses ON statuses.articleID = articles.articleID
            WHERE statuses.starred = 1
            ORDER BY articles.datePublished DESC
        """
        try:
            cur.execute(query)
            items = cur.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}\nCheck table/column names in your NetNewsWire database.")
            conn.close()
            return
        if not items:
            print("No favourited articles found.")
        from urllib.parse import urlparse
        from collections import defaultdict

        # Group articles by top-level domain
        domain_groups = defaultdict(list)
        for title, summary, url, external_url in items:
            safe_title = title if title else "(No Title)"
            chosen_url = external_url if external_url else url
            safe_url = chosen_url if chosen_url else None
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
        frontmatter = (
            '---\n'
            f'title: "RSS Favourites Digest: {month_year}"\n'
            f'date: {now.strftime('%Y-%m-%d')}\n'
            'layout: post\n'
            'categories: [digest, netnewswire]\n'
            '---\n\n'
        )
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(f'# RSS Favourited Articles Digest — {month_year}\n\n')
            for tld in sorted(domain_groups.keys()):
                f.write(f'## {tld}\n\n')
                for safe_title, safe_url in domain_groups[tld]:
                    f.write(f'- [{safe_title}]({safe_url})\n')
                f.write('\n')
        print(f"Exported {sum(len(v) for v in domain_groups.values())} favourited articles to {OUTPUT_FILE}")
        conn.close()
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

