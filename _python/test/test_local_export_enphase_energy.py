import os
import sys
import types
from urllib.parse import parse_qs, urlparse

LOCAL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "local"))
if LOCAL_DIR not in sys.path:
    sys.path.insert(0, LOCAL_DIR)

# local/config.py is git-ignored and holds secrets, so stub it for import.
_had_config = "config" in sys.modules
_saved_config = sys.modules.get("config")
sys.modules["config"] = types.ModuleType("config")
try:
    import local_export_enphase_energy as enphase  # noqa: E402
finally:
    if _had_config:
        sys.modules["config"] = _saved_config
    else:
        del sys.modules["config"]

BASE = "https://api.enphaseenergy.com/oauth/authorize"
REDIRECT = enphase.REDIRECT_URI


def params(url):
    return {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}


def test_bare_auth_url_gets_response_type_client_id_and_redirect():
    url = enphase.build_auth_url(BASE, " abc123 ", REDIRECT)
    assert url.startswith(BASE + "?")
    assert params(url) == {
        "response_type": "code",
        "client_id": "abc123",
        "redirect_uri": REDIRECT,
    }


def test_portal_url_with_params_is_not_duplicated():
    portal = f"{BASE}?response_type=code&client_id=abc123"
    url = enphase.build_auth_url(portal, "abc123", REDIRECT)
    assert url.count("client_id=") == 1
    assert url.count("response_type=") == 1
    assert params(url)["redirect_uri"] == REDIRECT


def test_existing_redirect_uri_is_kept_once():
    portal = f"{BASE}?response_type=code&client_id=abc123&redirect_uri=x"
    url = enphase.build_auth_url(portal, "abc123", REDIRECT)
    assert url.count("redirect_uri=") == 1
