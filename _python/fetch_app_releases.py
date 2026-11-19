"""Release posts for the private iOS and Mac app repos.

Their GitHub release feeds aren't public, so fetch_releases.py can't read
them. This reads the latest release of each repo in _data/app_releases.yml
through the GitHub API (token in APP_RELEASES_TOKEN, or GH_TOKEN locally) and
writes a release post to _posts/yyyy/ with an About section from the app's
_projects file and a What's Changed section from the release notes, which
the shared apple-release workflow takes from the [Release] commit body.

The filename ends in a hash of the project and tag, so a release is only
ever posted once. Posts link to the App Store, not the private repo.
"""
import os
import re
import pathlib
from datetime import datetime
from urllib.parse import urlparse

import requests
import yaml

import fetch_releases
import helper

ROOT = pathlib.Path(__file__).parent.parent.resolve()
CONFIG_FILE = ROOT / "_data" / "app_releases.yml"
PROJECTS_DIR = ROOT / "_projects"
POSTS_DIR = ROOT / "_posts"
OWNER = "thechelsuk"
API = "https://api.github.com"
APP_SEO_PADDING = ("See what changed in this version. "
                   "Read more about all my apps and tools on the "
                   "projects page.")


def load_config(path: pathlib.Path) -> list[dict[str, str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise ValueError(f"{path} must be a list of id, repo, project")
    for item in data:
        if not all(k in item for k in ("id", "repo", "project")):
            raise ValueError(
                f"Each entry needs id, repo and project: {item!r}")
    return data


def load_project(projects_dir: pathlib.Path, name: str) -> dict:
    text = (projects_dir / f"{name}.md").read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def fetch_latest_release(repo: str, token: str) -> dict | None:
    """GitHub's latest release only, so quick-fire releases post once."""
    resp = requests.get(
        f"{API}/repos/{OWNER}/{repo}/releases/latest",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=30,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def clean_notes(notes: str) -> str:
    """Notes as tidy markdown: no CRs or non-breaking spaces."""
    text = (notes or "").replace("\r\n", "\n").replace("\r", "\n")
    return fetch_releases.normalise_markdown(text.replace("\u00a0", " "))


def changelog(notes: str) -> str:
    """Release notes as a bullet list (plain lines become bullets)."""
    text = clean_notes(notes)
    lines = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith(("-", "*", "#")) or line[:1].isdigit():
            lines.append(line)
        else:
            lines.append(f"- {line.strip()}")
    return "\n".join(lines) or fetch_releases.NO_RELEASE_NOTES


def build_body(label: str, project: dict, notes: str) -> str:
    summary = str(project.get("summary") or project.get("pitch") or "")
    more = project.get("site_url") or project.get("permalink")
    about = summary.strip()
    if more:
        about = f"{about}\n\nMore about [{label}]({more})."
    return (f"## About\n\n{about}\n\n"
            f"## What's Changed\n\n{changelog(changes_only(notes))}")


def changes_only(notes: str) -> str:
    """The notes' own What's Changed section if they have one, else all of
    them. Any About in the notes is dropped: About comes from _projects."""
    text = clean_notes(notes)
    match = re.search(r"^##\s*What.s Changed\s*$(.*?)(?=^##\s|\Z)", text,
                      re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


def _on_host(host: str, domain: str) -> bool:
    return host == domain or host.endswith("." + domain)


def cited_for(link: str) -> str:
    host = (urlparse(link).hostname or "").lower()
    if _on_host(host, "apps.apple.com"):
        return "App Store"
    if _on_host(host, "gumroad.com"):
        return "Gumroad"
    return "thechels.uk"


def build_record(entry: dict, project: dict, release: dict) -> \
        fetch_releases.ReleaseRecord:
    label = entry["id"]
    repo = entry["repo"]
    version = release["tag_name"]
    link = project.get("i_url") or project.get("site_url") or "/projects"
    published = helper.parse_published(
        release.get("published_at") or release["created_at"])
    if not isinstance(published, datetime):
        raise ValueError(f"Bad release date for {repo} {version}")
    return fetch_releases.ReleaseRecord(
        project_key=fetch_releases.derive_project_key(label),
        project_label=label,
        repo_name=repo,
        release_id=f"github-release:{OWNER}/{repo.lower()}/{version}",
        version=version,
        link=link,
        published=published,
        body=build_body(label, project,
                        release.get("body") or ""),
        cited=cited_for(link),
        seo_padding=APP_SEO_PADDING,
    )


def process_app_releases(config_file: pathlib.Path = CONFIG_FILE,
                         projects_dir: pathlib.Path = PROJECTS_DIR,
                         posts_root: pathlib.Path = POSTS_DIR,
                         token: str | None = None) -> tuple[int, int, int]:
    if token is None:
        token = (os.environ.get("APP_RELEASES_TOKEN")
                 or os.environ.get("GH_TOKEN") or "")
    if not token:
        print("No APP_RELEASES_TOKEN set, skipping private app releases.")
        return 0, 0, 0

    created = skipped = failed = 0
    for entry in load_config(config_file):
        try:
            release = fetch_latest_release(entry["repo"], token)
            if release is None:
                skipped += 1
                continue
            project = load_project(projects_dir, entry["project"])
            record = build_record(entry, project, release)
            if fetch_releases.create_release_post(posts_root, record):
                created += 1
            else:
                skipped += 1
        except Exception as exc:
            failed += 1
            print(f"Failed to process {entry['repo']}: {exc}")
    return created, skipped, failed


if __name__ == "__main__":
    c, s, f = process_app_releases()
    print(f"App releases completed: {c} created, {s} skipped, {f} failed")
