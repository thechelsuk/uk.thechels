import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pytest
import yaml
import seo_frontmatter

TITLE = "A title that is long enough for search"
DESCRIPTION = ("A description that is long enough to satisfy the minimum "
               "length check, written with \"quotes\" and a colon: to test "
               "escaping.")


def front_matter(text):
    return yaml.safe_load(seo_frontmatter.split_front_matter(text)[1])


class TestSeoFrontmatter:

    def test_set_seo_inserts_after_title_and_removes_legacy(self):
        text = "---\nlayout: post\ntitle: Hello\nseo: old\n---\n\nBody\n"
        updated = seo_frontmatter.set_seo(text, TITLE, DESCRIPTION)
        data = front_matter(updated)
        assert data["seo_title"] == TITLE
        assert data["seo_description"] == DESCRIPTION
        assert "seo" not in data
        assert updated.splitlines()[3].startswith("seo_title:")
        assert updated.endswith("---\n\nBody\n")

    def test_set_seo_replaces_existing_values(self):
        text = ("---\ntitle: Hello\nseo_title: old\n"
                "seo_description: old\n---\nBody\n")
        updated = seo_frontmatter.set_seo(text, TITLE, DESCRIPTION)
        assert updated.count("seo_title:") == 1
        assert front_matter(updated)["seo_title"] == TITLE

    def test_set_seo_rejects_block_scalars(self):
        text = "---\ntitle: Hello\nseo: >\n  folded\n---\nBody\n"
        with pytest.raises(ValueError):
            seo_frontmatter.set_seo(text, TITLE, DESCRIPTION)

    def test_rename_seo(self):
        text = "---\ntitle: Hello\nseo: Kept text\n---\nBody\n"
        data = front_matter(seo_frontmatter.rename_seo(text))
        assert data["seo_description"] == "Kept text"
        assert "seo" not in data

    def test_rename_seo_keeps_existing_description(self):
        text = "---\nseo: old\nseo_description: new\n---\nBody\n"
        assert seo_frontmatter.rename_seo(text) == text

    def test_check_lengths(self):
        assert seo_frontmatter.check_lengths(TITLE, DESCRIPTION) == []
        assert len(seo_frontmatter.check_lengths("short", "short")) == 2
