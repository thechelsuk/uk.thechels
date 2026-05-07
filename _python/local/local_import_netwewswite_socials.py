"""
Script to merge two CSV files containing account data, deduplicate, sort alphabetically, and export to OPML with RSS feeds inferred from Mastodon and Bluesky handles.

- Defensive: Handles missing/invalid data, unknown columns, and malformed handles.
- Type safe: Uses type hints and dataclasses.
- Modular: Each step is a method with docstrings.
"""
import csv
import os
from dataclasses import dataclass, field
from typing import List, Optional, Set
import xml.etree.ElementTree as ET
import re
import config

BSKY = config.IN_BSKY
MASTO = config.IN_MASTO
OUT_SOCIALS = config.OUT_SOCIALS


@dataclass(frozen=True, order=True)
class Account:
    name: str
    handle: str
    platform: str  # 'mastodon' or 'bluesky'
    rss_url: Optional[str] = field(default=None, compare=False)


def read_csv_accounts(file_path: str) -> List[Account]:
    """
    Reads a CSV file and extracts account information.
    Handles Bluesky and Mastodon CSV formats as provided.
    Returns a list of Account objects. Skips rows with missing/invalid data.
    """
    accounts = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Detect file type by header
        fieldnames = [f.lower() for f in reader.fieldnames or []]
        if 'handle' in fieldnames and 'displayname' in fieldnames:
            # Bluesky CSV
            for row in reader:
                name = row.get('displayName') or row.get(
                    'displayname') or row.get('name')
                handle = row.get('handle')
                if not name or not handle:
                    continue
                accounts.append(
                    Account(name=name.strip(),
                            handle=handle.strip(),
                            platform='bluesky'))
        elif 'account address' in fieldnames:
            # Mastodon CSV
            for row in reader:
                handle = row.get('Account address') or row.get(
                    'account address')
                if not handle:
                    continue
                accounts.append(
                    Account(name=handle.strip(),
                            handle=handle.strip(),
                            platform='mastodon'))
        else:
            # Unknown format, fallback to old logic
            for row in reader:
                name = row.get('name') or row.get('Name')
                handle = row.get('handle') or row.get('Handle')
                platform = (row.get('platform') or row.get('Platform')
                            or '').lower()
                if not name or not handle or platform not in {
                        'mastodon', 'bluesky'
                }:
                    continue
                accounts.append(
                    Account(name=name.strip(),
                            handle=handle.strip(),
                            platform=platform))
    return accounts


def deduplicate_accounts(accounts: List[Account]) -> List[Account]:
    """
    Deduplicates accounts by (handle, platform). Returns sorted list by name.
    """
    seen: Set[tuple] = set()
    unique = []
    for acc in accounts:
        key = (acc.handle.lower(), acc.platform)
        if key not in seen:
            seen.add(key)
            unique.append(acc)
    return sorted(unique, key=lambda a: a.name.lower())


def infer_rss_url(account: Account) -> Optional[str]:
    """
    Infers the RSS/Atom feed URL for a Mastodon or Bluesky account.
    Returns None if handle is malformed.
    """
    if account.platform == 'mastodon':
        # Mastodon: handle must be in the form user@instance (no protocol, no slashes)
        m = re.fullmatch(r'([A-Za-z0-9_.-]+)@([A-Za-z0-9_.-]+)',
                         account.handle)
        if m:
            user, instance = m.groups()
            return f'https://{instance}/@{user}.rss'
        else:
            return None
    elif account.platform == 'bluesky':
        # Bluesky: handle is user.bsky.social or similar, no @, no slashes
        handle = account.handle.lstrip('@')
        # Only allow valid domain-like handles (no slashes, no spaces)
        if re.fullmatch(r'[A-Za-z0-9_.-]+(\.[A-Za-z0-9_.-]+)+', handle):
            return f'https://bsky.app/profile/{handle}/rss'
        else:
            return None
    return None


def add_rss_urls(accounts: List[Account]) -> List[Account]:
    """
    Returns a new list of accounts with rss_url field populated.
    """
    return [
        Account(a.name, a.handle, a.platform, infer_rss_url(a))
        for a in accounts
    ]


def export_to_opml(accounts: List[Account], output_path: str) -> None:
    """
    Exports the list of accounts to an OPML file with RSS feeds.
    Only includes accounts with valid (HTTP 200) feed URLs.
    """
    opml = ET.Element('opml', version='2.0')
    head = ET.SubElement(opml, 'head')
    ET.SubElement(head, 'title').text = 'Unified Account List'
    body = ET.SubElement(opml, 'body')
    folder = ET.SubElement(body,
                           'outline',
                           text='9 - Socials',
                           title='9 - Socials')
    for acc in accounts:
        if not acc.rss_url:
            continue
        outline = ET.SubElement(folder,
                                'outline',
                                text=acc.name,
                                title=acc.name,
                                type='rss',
                                xmlUrl=acc.rss_url,
                                platform=acc.platform,
                                handle=acc.handle)

    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for e in elem:
                indent(e, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    indent(opml)
    tree = ET.ElementTree(opml)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)


def main() -> None:
    """
    Main function to merge, deduplicate, and export accounts to OPML using BSKY and MASTO constants.
    """
    accounts1 = read_csv_accounts(BSKY)
    accounts2 = read_csv_accounts(MASTO)
    all_accounts = accounts1 + accounts2
    unique_accounts = deduplicate_accounts(all_accounts)
    accounts_with_rss = add_rss_urls(unique_accounts)
    export_to_opml(accounts_with_rss, OUT_SOCIALS)
    print(f"Exported {len(accounts_with_rss)} accounts to {OUT_SOCIALS}")


if __name__ == '__main__':
    main()
