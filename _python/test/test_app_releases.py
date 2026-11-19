import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import fetch_app_releases as app_releases  # noqa: E402

PROJECT = ("---\n"
           "layout: projects\n"
           'title: "Lansdown Foundry: Make Fonts"\n'
           "permalink: /projects/foundry\n"
           'site_url: "https://lansdownfoundry.thechels.uk"\n'
           'i_url: "https://apps.apple.com/gb/app/lansdown-foundry/id1"\n'
           'summary: "Draw your own fonts on iPad and Mac."\n'
           "---\n\nBody\n")

API_RELEASE = {
    "tag_name":
    "v202701.3",
    "name":
    "202701.3",
    "html_url":
    "https://github.com/thechelsuk/repo/releases/tag/v202701.3",
    "published_at":
    "2026-11-19T03:15:55Z",
    "body": ("updated settings and duo screenshots\n\n"
             "Signed-off-by: thechelsuk <x@example.com>"),
    "draft":
    False,
}


def write_setup(tmp_path):
    projects = tmp_path / "_projects"
    projects.mkdir()
    (projects / "app-lansdown-foundry.md").write_text(PROJECT,
                                                      encoding="utf-8")
    config = tmp_path / "app_releases.yml"
    config.write_text(
        "- id: Lansdown Foundry\n"
        "  repo: com.uk.thechels.lansdownfoundry\n"
        "  project: app-lansdown-foundry\n",
        encoding="utf-8")
    return config, projects, tmp_path / "_posts"


def run(tmp_path, monkeypatch, releases):
    config, projects, posts = write_setup(tmp_path)
    monkeypatch.setattr(app_releases, "fetch_latest_release",
                        lambda repo, token: releases.get(repo))
    return app_releases.process_app_releases(config_file=config,
                                             projects_dir=projects,
                                             posts_root=posts,
                                             token="t"), posts


def test_creates_release_post_in_posts_year_with_about_and_changelog(
        tmp_path, monkeypatch):
    counts, posts = run(tmp_path, monkeypatch,
                        {"com.uk.thechels.lansdownfoundry": API_RELEASE})
    assert counts == (1, 0, 0)
    files = list(posts.rglob("*.md"))
    assert len(files) == 1
    path = files[0]
    assert path.parent == posts / "2026"
    assert path.name.startswith("2026-11-19-lansdown-foundry-release-")
    assert path.stem.rsplit("-", 1)[-1].isalnum()
    text = path.read_text(encoding="utf-8")
    assert "type: release" in text
    assert "title: Lansdown Foundry Version v202701.3" in text
    assert "## About\n\nDraw your own fonts on iPad and Mac." in text
    assert "[Lansdown Foundry](https://lansdownfoundry.thechels.uk)" in text
    assert "## What's Changed\n\n- updated settings and duo screenshots" in text
    assert "Signed-off-by" not in text
    assert "x@example.com" not in text


def test_links_to_app_store_not_private_github(tmp_path, monkeypatch):
    _, posts = run(tmp_path, monkeypatch,
                   {"com.uk.thechels.lansdownfoundry": API_RELEASE})
    text = next(posts.rglob("*.md")).read_text(encoding="utf-8")
    assert "link: https://apps.apple.com/gb/app/lansdown-foundry/id1" in text
    assert "cited: App Store" in text
    assert "github.com" not in text


def test_seo_description_makes_no_open_source_claim(tmp_path, monkeypatch):
    release = dict(API_RELEASE, body="- fix")
    _, posts = run(tmp_path, monkeypatch,
                   {"com.uk.thechels.lansdownfoundry": release})
    text = next(posts.rglob("*.md")).read_text(encoding="utf-8")
    assert "open source" not in text


def test_second_run_skips_duplicate(tmp_path, monkeypatch):
    run(tmp_path, monkeypatch,
        {"com.uk.thechels.lansdownfoundry": API_RELEASE})
    monkeypatch.setattr(app_releases, "fetch_latest_release",
                        lambda repo, token: API_RELEASE)
    config = tmp_path / "app_releases.yml"
    counts = app_releases.process_app_releases(config_file=config,
                                               projects_dir=tmp_path /
                                               "_projects",
                                               posts_root=tmp_path / "_posts",
                                               token="t")
    assert counts == (0, 1, 0)
    assert len(list((tmp_path / "_posts").rglob("*.md"))) == 1


def test_repo_with_no_release_is_skipped(tmp_path, monkeypatch):
    counts, posts = run(tmp_path, monkeypatch, {})
    assert counts == (0, 1, 0)
    assert not posts.exists() or not list(posts.rglob("*.md"))


def test_no_token_does_nothing(tmp_path):
    config, projects, posts = write_setup(tmp_path)
    counts = app_releases.process_app_releases(config_file=config,
                                               projects_dir=projects,
                                               posts_root=posts,
                                               token="")
    assert counts == (0, 0, 0)


def test_empty_notes_get_placeholder(tmp_path, monkeypatch):
    release = dict(API_RELEASE, body="")
    _, posts = run(tmp_path, monkeypatch,
                   {"com.uk.thechels.lansdownfoundry": release})
    text = next(posts.rglob("*.md")).read_text(encoding="utf-8")
    assert "No release notes were included for this release." in text


def test_existing_bullets_are_kept():
    assert app_releases.changelog("- one\n- two") == "- one\n- two"
    assert app_releases.changelog("one\ntwo") == "- one\n- two"


def test_about_always_from_project_and_only_changes_from_notes():
    notes = ("##\u00a0About\r\n\r\nTurns reports into something readable.\r\n"
             "## What's Changed\r\n- First release")
    body = app_releases.build_body(
        "Demarkable", {
            "summary": "Summary from front matter.",
            "permalink": "/projects/demarkable"
        }, notes)
    assert body.count("## About") == 1
    assert body.count("## What's Changed") == 1
    assert "## About\n\nSummary from front matter." in body
    assert "Turns reports" not in body
    assert "\r" not in body
    assert body.endswith("## What's Changed\n\n- First release")


def test_cited_follows_store_link():
    assert app_releases.cited_for(
        "https://apps.apple.com/gb/app/x/id1") == "App Store"
    assert app_releases.cited_for(
        "https://thechelsuk.gumroad.com/l/dmarc") == "Gumroad"


def test_more_about_links_to_marketing_site_when_there_is_one():
    body = app_releases.build_body(
        "Tomoz", {
            "summary": "S.",
            "permalink": "/projects/tomoz",
            "site_url": "https://tomoz.thechels.uk"
        }, "- x")
    assert "More about [Tomoz](https://tomoz.thechels.uk)." in body
    assert "/projects/tomoz" not in body


def test_more_about_falls_back_to_project_page():
    body = app_releases.build_body("Demarkable", {
        "summary": "S.",
        "permalink": "/projects/demarkable"
    }, "- x")
    assert "More about [Demarkable](/projects/demarkable)." in body


class FakeResponse:

    def __init__(self, status, data=None):
        self.status_code = status
        self._data = data

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)


def test_fetch_asks_github_for_the_latest_release_only(monkeypatch):
    calls = []

    def fake_get(url, **kwargs):
        calls.append(url)
        return FakeResponse(200, {"tag_name": "v1.9"})

    monkeypatch.setattr(app_releases.requests, "get", fake_get)
    release = app_releases.fetch_latest_release("repo", "t")
    assert release == {"tag_name": "v1.9"}
    assert calls == [
        f"{app_releases.API}/repos/thechelsuk/repo/releases/latest"
    ]


def test_fetch_returns_none_when_repo_has_no_release(monkeypatch):
    monkeypatch.setattr(app_releases.requests, "get",
                        lambda url, **kwargs: FakeResponse(404))
    assert app_releases.fetch_latest_release("repo", "t") is None
