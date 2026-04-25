import html
import hashlib
import pathlib
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.parse import unquote, urlparse
import feedparser
from markdownify import markdownify as convert_html
import yaml
import helper

ROOT = pathlib.Path(__file__).parent.parent.resolve()
FEEDS_FILE = ROOT / "_data" / "releases.yml"
POSTS_DIR = ROOT / "_posts"
NO_RELEASE_NOTES = "No release notes were included for this release."


@dataclass(frozen=True)
class ReleaseRecord:
    project_key: str
    project_label: str
    repo_name: str
    release_id: str
    version: str
    link: str
    published: datetime
    body: str

    @property
    def release_hash(self) -> str:
        identity = f"{self.project_key}:{self.release_id or self.link}"
        return hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]

    @property
    def filename(self) -> str:
        date_part = self.published.date().isoformat()
        return f"{date_part}-{self.project_key}-release-{self.release_hash}.md"

    @property
    def title(self) -> str:
        return f"{self.project_label} Version {self.version}"


def load_release_feeds(file_path: pathlib.Path) -> list[dict[str, str]]:
    raw = file_path.read_text(encoding="utf-8")
    if not raw.strip():
        return []

    data = yaml.safe_load(raw)
    if not isinstance(data, list):
        raise ValueError(
            "Release feeds file must contain a list of entries with id and url keys"
        )

    result = []
    for item in data:
        if not isinstance(item, dict) or "id" not in item or "url" not in item:
            raise ValueError(
                f"Each entry must have 'id' and 'url' keys, got: {item!r}")
        result.append({
            "id": str(item["id"]).strip(),
            "url": str(item["url"]).strip()
        })
    return result


def extract_repo_name(feed_url: str) -> str:
    parsed = urlparse(feed_url)
    match = re.match(r"^/[^/]+/([^/]+)/releases\.atom$", parsed.path)
    if not match:
        raise ValueError(f"Unsupported GitHub release feed URL: {feed_url}")
    return match.group(1)


def derive_project_key(label: str) -> str:
    key = label.strip().lower()
    key = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    if not key:
        raise ValueError(f"Unable to derive project key from: {label}")
    return key


def extract_release_version(entry: Any) -> str:
    link = str(get_entry_value(entry, "link", "") or "").strip()
    match = re.search(r"/releases/tag/([^/?#]+)", link)
    if match:
        return unquote(match.group(1)).strip()

    release_id = str(get_entry_value(entry, "id", "") or "").strip()
    if release_id and "/" in release_id:
        return release_id.rsplit("/", 1)[-1].strip()

    return str(get_entry_value(entry, "title", "") or "").strip()


def get_entry_value(entry: Any, key: str, default: Any = None) -> Any:
    if hasattr(entry, "get"):
        return entry.get(key, default)
    return getattr(entry, key, default)


def get_content_value(content_item: Any) -> str:
    if hasattr(content_item, "get"):
        return str(content_item.get("value", "") or "")
    return str(getattr(content_item, "value", "") or "")


def normalise_markdown(value: str) -> str:
    text = "\n".join(line.rstrip() for line in value.splitlines())
    text = text.replace("[bot]", "")
    text = re.sub(r"<(https?://[^>]+)>", r"[\1](\1)", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_to_markdown(value: str) -> str:
    content = value.strip()
    if not content:
        return ""

    if not re.search(r"<[^>]+>", content):
        return normalise_markdown(html.unescape(content))

    markdown = convert_html(content,
                            heading_style="ATX",
                            bullets="-",
                            escape_asterisks=False,
                            escape_underscores=False)
    return normalise_markdown(markdown)


def build_release_body(entry: Any) -> str:
    content = get_entry_value(entry, "content", []) or []
    body = ""
    if content:
        body = get_content_value(content[0]).strip()

    if not body or body == "No content.":
        body = str(get_entry_value(entry, "summary", "") or "").strip()

    if not body or body == "No content.":
        return NO_RELEASE_NOTES

    markdown = html_to_markdown(body)
    return markdown or NO_RELEASE_NOTES


def parse_release_datetime(entry: Any) -> datetime:
    published = str(get_entry_value(entry, "published", "") or "").strip()
    updated = str(get_entry_value(entry, "updated", "") or "").strip()
    value = published or updated
    if not value:
        raise ValueError(
            "Release entry is missing a published or updated date")
    return helper.parse_published(value)


def build_release_record(feed_url: str, entry: Any,
                         project_id: str) -> ReleaseRecord:
    repo_name = extract_repo_name(feed_url)
    project_key = derive_project_key(project_id)
    project_label = project_id
    link = str(get_entry_value(entry, "link", "") or "").strip()
    version = extract_release_version(entry)
    release_id = str(get_entry_value(entry, "id", "") or link).strip()

    if not version:
        raise ValueError(f"Release entry from {feed_url} is missing a title")
    if not link:
        raise ValueError(f"Release entry from {feed_url} is missing a link")
    if not release_id:
        raise ValueError(f"Release entry from {feed_url} is missing an id")

    return ReleaseRecord(
        project_key=project_key,
        project_label=project_label,
        repo_name=repo_name,
        release_id=release_id,
        version=version,
        link=link,
        published=parse_release_datetime(entry),
        body=build_release_body(entry),
    )


def render_post(release: ReleaseRecord) -> str:
    # Intercept NetNewsWire theme URL in body (plain or markdownified)
    body = release.body.strip() or NO_RELEASE_NOTES
    download_url = None
    # Regex for both plain and markdownified NetNewsWire theme URLs
    nnw_patterns = [
        re.compile(r"^netnewswire://theme/add\?url=(https://[\w./%\-]+\.zip)$",
                   re.MULTILINE),
        re.compile(
            r"^netnewswire://theme/add\?url=\[(https://[\w./%\-]+\.zip)\]\(https://[\w./%\-]+\.zip\)$",
            re.MULTILINE),
    ]
    match = None
    for pattern in nnw_patterns:
        matches = list(pattern.finditer(body))
        if matches:
            match = matches[-1]
            break
    if match:
        download_url = match.group(1)
        # Replace only the last occurrence with the install link
        start, end = match.span()
        body = body[:
                    start] + f"[Install now](netnewswire://theme/add?url={{page.download}})" + body[
                        end:]
        # Clean up any extra blank lines (optional, but keeps formatting tidy)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()

    front_matter = {
        "layout": "post",
        "date": release.published.date().isoformat(),
        "title": release.title,
        "type": "release",
        "cited": "github",
        "link": release.link,
        "release_id": release.release_id,
        "release_repo": release.repo_name,
        "release_project": release.project_key,
        "release_version": release.version,
    }
    if download_url:
        front_matter["download"] = download_url

    yaml_front_matter = yaml.safe_dump(front_matter,
                                       sort_keys=False,
                                       allow_unicode=False).strip()
    return f"---\n{yaml_front_matter}\n---\n\n{body}\n"


def find_existing_post(posts_root: pathlib.Path, project_key: str,
                       release_hash: str) -> pathlib.Path | None:
    pattern = f"*-{project_key}-release-{release_hash}.md"
    return next(posts_root.rglob(pattern), None)


def create_release_post(posts_root: pathlib.Path,
                        release: ReleaseRecord) -> bool:
    existing = find_existing_post(posts_root, release.project_key,
                                  release.release_hash)
    if existing:
        return False

    destination_dir = posts_root / str(release.published.year)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / release.filename
    destination.write_text(render_post(release), encoding="utf-8")
    return True


def fetch_feed_releases(feed_url: str, project_id: str) -> list[ReleaseRecord]:
    feed = feedparser.parse(feed_url)
    result = []
    # Only process the latest entry (if any)
    for entry in getattr(feed, "entries", [])[:1]:
        result.append(build_release_record(feed_url, entry, project_id))
    return result


def process_releases(
        feeds_file: pathlib.Path = FEEDS_FILE,
        posts_root: pathlib.Path = POSTS_DIR) -> tuple[int, int, int]:
    created = 0
    skipped = 0
    failed = 0

    for feed_config in load_release_feeds(feeds_file):
        feed_url = feed_config["url"]
        project_id = feed_config["id"]
        try:
            for release in fetch_feed_releases(feed_url, project_id):
                if create_release_post(posts_root, release):
                    created += 1
                else:
                    skipped += 1
        except Exception as exc:
            failed += 1
            print(f"Failed to process {feed_url}: {exc}")

    return created, skipped, failed


if __name__ == "__main__":
    try:
        created_count, skipped_count, failed_count = process_releases()
        print(
            f"Releases completed: {created_count} created, {skipped_count} skipped, {failed_count} failed"
        )
    except FileNotFoundError:
        print("File does not exist, unable to proceed")
