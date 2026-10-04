# importing modules
import argparse
import pathlib

from PIL import Image, ImageOps

# defaults suit the site: mixtapes are 832px wide, quality 80 is visually
# lossless for photos and album art at a fraction of the PNG size
DEFAULT_WIDTH = 832
DEFAULT_QUALITY = 80


def convert(source, target=None, width=DEFAULT_WIDTH, quality=DEFAULT_QUALITY):
    """Save source as a WebP no wider than width and return the target path.

    Convert from the full colour original, not a colour reduced copy: WebP
    compresses dithering noise badly, so a 24 colour PNG can come out larger.
    """
    source = pathlib.Path(source)
    target = pathlib.Path(target) if target else source.with_suffix(".webp")
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        has_alpha = image.mode in ("RGBA", "LA") or "transparency" in image.info
        image = image.convert("RGBA" if has_alpha else "RGB")
        if width and image.width > width:
            height = round(image.height * width / image.width)
            image = image.resize((width, height), Image.LANCZOS)
        image.save(target, "WEBP", quality=quality, method=6)
    return target


def kilobytes(path):
    return pathlib.Path(path).stat().st_size / 1024


# processing
if __name__ == "__main__":
    arguments = argparse.ArgumentParser(
        description="""Convert images to resized WebP files.""")
    arguments.add_argument("images", nargs="+", help="Images to convert")
    arguments.add_argument("-o", "--output",
                           help="Output file (one image) or folder")
    arguments.add_argument("-w", "--width", type=int, default=DEFAULT_WIDTH,
                           help=f"Maximum width in px, 0 to keep "
                           f"(default {DEFAULT_WIDTH})")
    arguments.add_argument("-q", "--quality", type=int,
                           default=DEFAULT_QUALITY,
                           help=f"WebP quality 0-100 (default {DEFAULT_QUALITY})")
    args = arguments.parse_args()

    output = pathlib.Path(args.output) if args.output else None
    for image in args.images:
        target = output
        if output and (output.is_dir() or len(args.images) > 1):
            output.mkdir(parents=True, exist_ok=True)
            target = output / pathlib.Path(image).with_suffix(".webp").name
        result = convert(image, target, args.width, args.quality)
        print(f"{image} ({kilobytes(image):.0f} KB) -> "
              f"{result} ({kilobytes(result):.0f} KB)")
