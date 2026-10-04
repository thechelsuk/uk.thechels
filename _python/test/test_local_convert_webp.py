import os
import sys

LOCAL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "local"))
if LOCAL_DIR not in sys.path:
    sys.path.insert(0, LOCAL_DIR)

from PIL import Image  # noqa: E402
import local_convert_webp  # noqa: E402


def make_image(path, size=(1000, 500), mode="RGB", colour=(200, 50, 50)):
    if mode == "RGBA":
        colour = colour + (128, )
    Image.new(mode, size, colour).save(path)
    return path


def test_convert_writes_webp_next_to_source(tmp_path):
    source = make_image(tmp_path / "2026-10.png")
    target = local_convert_webp.convert(source)
    assert target == tmp_path / "2026-10.webp"
    with Image.open(target) as image:
        assert image.format == "WEBP"


def test_convert_resizes_to_width_keeping_aspect(tmp_path):
    source = make_image(tmp_path / "wide.png", size=(1000, 500))
    target = local_convert_webp.convert(source, width=832)
    with Image.open(target) as image:
        assert image.size == (832, 416)


def test_convert_does_not_upscale(tmp_path):
    source = make_image(tmp_path / "small.png", size=(400, 300))
    target = local_convert_webp.convert(source, width=832)
    with Image.open(target) as image:
        assert image.size == (400, 300)


def test_convert_width_zero_keeps_size(tmp_path):
    source = make_image(tmp_path / "big.png", size=(1200, 600))
    target = local_convert_webp.convert(source, width=0)
    with Image.open(target) as image:
        assert image.size == (1200, 600)


def test_convert_keeps_transparency(tmp_path):
    source = make_image(tmp_path / "alpha.png", mode="RGBA")
    target = local_convert_webp.convert(source)
    with Image.open(target) as image:
        assert image.mode == "RGBA"


def test_convert_custom_target(tmp_path):
    source = make_image(tmp_path / "in.jpeg")
    target = local_convert_webp.convert(source, tmp_path / "out.webp")
    assert target == tmp_path / "out.webp"
    assert target.exists()
