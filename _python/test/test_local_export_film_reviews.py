import os
import sys
import types
from datetime import datetime

LOCAL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "local"))
if LOCAL_DIR not in sys.path:
    sys.path.insert(0, LOCAL_DIR)

# local/config.py is git-ignored and holds secrets, so stub it for import.
_had_config = "config" in sys.modules
_saved_config = sys.modules.get("config")
sys.modules["config"] = types.ModuleType("config")
try:
    import local_export_film_reviews  # noqa: E402
finally:
    if _had_config:
        sys.modules["config"] = _saved_config
    else:
        del sys.modules["config"]


def build():
    films = [(datetime(2026, 11, 1), {
        "title": "Nosferatu",
        "year": 2024,
        "rating": 8
    })]
    return local_export_film_reviews.build_post_content(films,
                                                        today=datetime(
                                                            2026, 11, 19, 13,
                                                            18))


def test_front_matter_has_syndicate_list():
    content = build()
    assert "syndicate:\n  - mastodon\n  - bluesky\n" in content


def test_front_matter_has_no_syndicate_false():
    assert "syndicate: false" not in build()
