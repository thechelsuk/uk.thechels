from datetime import datetime, timezone
from types import SimpleNamespace

import fetch_releases as fetch_releases


def make_entry(**overrides):
    entry = {
        "id":
        "tag:github.com,2008:Repository/1210963867/1.0.0",
        "title":
        "1.0.0",
        "link":
        "https://github.com/thechelsuk/uk.thechels.search/releases/tag/1.0.0",
        "updated":
        "2026-04-18T18:10:31Z",
        "content": [{
            "value":
            "<h2>What's Changed</h2><ul><li>Added search improvements</li></ul>"
        }],
        "summary":
        "Summary text",
    }
    entry.update(overrides)
    return entry


def test_extract_repo_name_from_feed_url():
    assert fetch_releases.extract_repo_name(
        "https://github.com/thechelsuk/uk.thechels.search/releases.atom"
    ) == "uk.thechels.search"


def test_derive_project_key():
    assert fetch_releases.derive_project_key(
        "Search Router") == "search-router"
    assert fetch_releases.derive_project_key("Mltply") == "mltply"
    assert fetch_releases.derive_project_key(
        "Cheltenham Open Data") == "cheltenham-open-data"
    assert fetch_releases.derive_project_key(
        "Boinc @ thechelsuk") == "boinc-thechelsuk"


def test_load_release_feeds_parses_id_and_url(tmp_path):
    feeds_file = tmp_path / "releases.yml"
    feeds_file.write_text(
        "- id: Search Router\n"
        "  url: https://github.com/thechelsuk/uk.thechels.search/releases.atom\n"
        "- id: Nuchronic.uk\n"
        "  url: https://github.com/thechelsuk/uk.nuchronic/releases.atom\n",
        encoding="utf-8",
    )

    assert fetch_releases.load_release_feeds(feeds_file) == [
        {
            "id": "Search Router",
            "url":
            "https://github.com/thechelsuk/uk.thechels.search/releases.atom"
        },
        {
            "id": "Nuchronic.uk",
            "url": "https://github.com/thechelsuk/uk.nuchronic/releases.atom"
        },
    ]


def test_extract_release_version_prefers_release_tag():
    entry = make_entry(title="Initial Release 1.0.0")
    assert fetch_releases.extract_release_version(entry) == "1.0.0"


def test_html_to_markdown_converts_release_notes_html():
    source = (
        "<h2>What's Changed</h2>"
        "<ul><li>Added search improvements in <a href=\"https://example.com/pr/1\">#1</a></li></ul>"
        "<p><strong>Full Changelog</strong>: <a href=\"https://example.com/changelog\">https://example.com/changelog</a></p>"
    )

    result = fetch_releases.html_to_markdown(source)
    assert "## What's Changed" in result
    assert "- Added search improvements in [#1](https://example.com/pr/1)" in result
    assert "**Full Changelog**: [https://example.com/changelog](https://example.com/changelog)" in result
    assert "<h2>" not in result
    assert "<p>" not in result


def test_html_to_markdown_strips_bot_suffixes():
    source = (
        "<ul><li>Bump dependency by <a href=\"https://github.com/dependabot\">@dependabot</a>[bot]"
        " in <a href=\"https://example.com/pr/2\">#2</a></li></ul>")

    result = fetch_releases.html_to_markdown(source)
    assert "[@dependabot](https://github.com/dependabot)" in result
    assert ")[bot]" not in result
    assert "[bot]" not in result


def test_build_release_body_uses_placeholder_when_feed_has_no_notes():
    entry = make_entry(content=[{"value": "No content."}], summary="")
    assert fetch_releases.build_release_body(
        entry) == fetch_releases.NO_RELEASE_NOTES


def test_build_release_body_returns_markdown_not_html():
    entry = make_entry()
    result = fetch_releases.build_release_body(entry)
    assert "## What's Changed" in result
    assert "- Added search improvements" in result
    assert "<h2>" not in result
    assert "<ul>" not in result


def test_build_release_body_removes_signed_off_by_lines():
    entry = make_entry(content=[{
        "value":
        "<p>Release notes line</p><p>Signed-off-by: Jane Doe &lt;jane@example.com&gt;</p><p>Another line</p>"
    }],
                       summary="")

    result = fetch_releases.build_release_body(entry)

    assert "Release notes line" in result
    assert "Another line" in result
    assert "Signed-off-by" not in result
    assert "jane@example.com" not in result


def test_build_release_record_uses_updated_timestamp_when_published_missing():
    release = fetch_releases.build_release_record(
        "https://github.com/thechelsuk/uk.thechels.search/releases.atom",
        make_entry(published=""),
        "Search Router",
    )
    assert release.project_key == "search-router"
    assert release.project_label == "Search Router"
    assert release.title == "Search Router Version 1.0.0"
    assert release.published == datetime(2026,
                                         4,
                                         18,
                                         18,
                                         10,
                                         31,
                                         tzinfo=timezone.utc)


def test_render_post_includes_required_front_matter():
    release = fetch_releases.ReleaseRecord(
        project_key="search",
        project_label="Search",
        repo_name="uk.thechels.search",
        release_id="tag:github.com,2008:Repository/1210963867/1.0.0",
        version="1.0.0",
        link=
        "https://github.com/thechelsuk/uk.thechels.search/releases/tag/1.0.0",
        published=datetime(2026, 4, 18, 18, 10, 31, tzinfo=timezone.utc),
        body="Release notes",
    )

    content = fetch_releases.render_post(release)
    assert "layout: post" in content
    assert "date: 2026-04-18 18:10" in content
    assert "date: '2026-04-18" not in content
    assert "type: release" in content
    assert "cited: github" in content
    assert "release_repo: uk.thechels.search" in content
    assert "release_project: search" in content
    assert "release_version: 1.0.0" in content
    assert "title: Search Version 1.0.0" in content
    assert "link: https://github.com/thechelsuk/uk.thechels.search/releases/tag/1.0.0" in content
    assert content.endswith(
        "Release notes\n\n[Read more about my projects](/projects/)\n")


def test_render_post_rewrites_labelled_netnewswire_links():
    release = fetch_releases.ReleaseRecord(
        project_key="nnw-thechelsuk-theme",
        project_label="NNW thechelsuk Theme",
        repo_name="uk.thechels.themes-for-nnw",
        release_id="tag:github.com,2008:Repository/1184541049/v1.4.0",
        version="v1.4.0",
        link=
        "https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/tag/v1.4.0",
        published=datetime(2026, 5, 1, 0, 0, 0, tzinfo=timezone.utc),
        body=
        ("## NetNewsWire Install Links\n\n"
         "- guro: netnewswire://theme/add?url=[https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/download/v1.4.0/guro.zip](https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/download/v1.4.0/guro.zip)\n"
         "- thechelsuk: netnewswire://theme/add?url=[https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/download/v1.4.0/thechelsuk.zip](https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/download/v1.4.0/thechelsuk.zip)"
         ),
    )

    content = fetch_releases.render_post(release)

    assert "- guro: [Install guro in NetNewsWire directly](netnewswire://theme/add?url=https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/download/v1.4.0/guro.zip)" in content
    assert "- thechelsuk: [Install thechelsuk in NetNewsWire directly](netnewswire://theme/add?url=https://github.com/thechelsuk/uk.thechels.themes-for-nnw/releases/download/v1.4.0/thechelsuk.zip)" in content
    assert "netnewswire://theme/add?url=[https://" not in content


def test_create_release_post_skips_when_hash_suffix_already_exists(tmp_path):
    release = fetch_releases.ReleaseRecord(
        project_key="search",
        project_label="Search",
        repo_name="uk.thechels.search",
        release_id="tag:github.com,2008:Repository/1210963867/1.0.0",
        version="1.0.0",
        link=
        "https://github.com/thechelsuk/uk.thechels.search/releases/tag/1.0.0",
        published=datetime(2026, 4, 18, 18, 10, 31, tzinfo=timezone.utc),
        body="Release notes",
    )
    existing_dir = tmp_path / "2026"
    existing_dir.mkdir(parents=True)
    existing_file = existing_dir / (
        f"2026-04-01-search-release-{release.release_hash}.md")
    existing_file.write_text("existing", encoding="utf-8")

    assert fetch_releases.create_release_post(tmp_path, release) is False
    assert existing_file.read_text(encoding="utf-8") == "existing"
    assert len(list(tmp_path.rglob("*.md"))) == 1


def test_process_releases_creates_new_posts_then_skips_duplicates(
        tmp_path, monkeypatch):
    feeds_file = tmp_path / "releases.yml"
    feeds_file.write_text(
        "- id: Search Router\n"
        "  url: https://github.com/thechelsuk/uk.thechels.search/releases.atom\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        fetch_releases.feedparser,
        "parse",
        lambda url: SimpleNamespace(entries=[make_entry()]),
    )

    first_created, first_skipped, first_failed = fetch_releases.process_releases(
        feeds_file=feeds_file,
        posts_root=tmp_path / "_posts",
    )
    second_created, second_skipped, second_failed = fetch_releases.process_releases(
        feeds_file=feeds_file,
        posts_root=tmp_path / "_posts",
    )

    assert (first_created, first_skipped, first_failed) == (1, 0, 0)
    assert (second_created, second_skipped, second_failed) == (0, 1, 0)

    generated_files = list((tmp_path / "_posts").rglob("*.md"))
    assert len(generated_files) == 1
    assert generated_files[0].name.startswith(
        "2026-04-18-search-router-release-")
    content = generated_files[0].read_text(encoding="utf-8")
    assert "title: Search Router Version 1.0.0" in content
    assert "cited: github" in content
    assert "## What's Changed" in content
    assert "<h2>" not in content
