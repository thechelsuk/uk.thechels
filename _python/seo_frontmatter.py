# importing modules
import argparse
import json
import pathlib
import re

import yaml

# limits based on what Google displays in search results
TITLE_MIN = 30
TITLE_MAX = 60
DESCRIPTION_MIN = 120
DESCRIPTION_MAX = 160

ROOT = pathlib.Path(__file__).parent.parent.resolve()
CONTENT_DIRS = ["_pages", "_posts", "_projects", "_bookmarks", "_rides"]
SEO_KEYS = ("seo", "seo_title", "seo_description")

# collections that are noindex by default in _config.yml
NOINDEX_DIRS = ["_bookmarks"]

FRONT_MATTER = re.compile(r"\A(\s*---[ \t]*\n)(.*?\n)(---[ \t]*\n)", re.S)
KEY_LINE = re.compile(r"^(?P<key>[A-Za-z_][\w-]*)\s*:")


def split_front_matter(text):
    """Return (opening, front matter body, rest) or None."""
    match = FRONT_MATTER.match(text)
    if not match:
        return None
    return match.group(1), match.group(2), text[match.start(3):]


def quote(value):
    """Return a double quoted YAML scalar."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def check_lengths(title, description):
    """Return a list of problems with the seo values."""
    problems = []
    if not TITLE_MIN <= len(title) <= TITLE_MAX:
        problems.append(f"seo_title is {len(title)} chars "
                        f"(want {TITLE_MIN}-{TITLE_MAX})")
    if not DESCRIPTION_MIN <= len(description) <= DESCRIPTION_MAX:
        problems.append(f"seo_description is {len(description)} chars "
                        f"(want {DESCRIPTION_MIN}-{DESCRIPTION_MAX})")
    return problems


def remove_keys(lines, keys):
    """Remove single line keys, refusing block scalars."""
    kept = []
    skipping = False
    for line in lines:
        match = KEY_LINE.match(line)
        if match:
            skipping = match.group("key") in keys
            if skipping and re.search(r":\s*[|>][-+]?\s*$", line):
                raise ValueError(f"block scalar not supported: {line!r}")
        elif not (skipping and line.startswith((" ", "\t"))):
            skipping = False
        if not skipping:
            kept.append(line)
    return kept


def set_seo(text, title, description):
    """Return text with seo_title and seo_description set after title."""
    parts = split_front_matter(text)
    if parts is None:
        raise ValueError("no front matter")
    opening, body, rest = parts
    lines = remove_keys(body.splitlines(keepends=True), SEO_KEYS)
    new_lines = [
        f"seo_title: {quote(title)}\n",
        f"seo_description: {quote(description)}\n",
    ]
    position = next(
        (i + 1 for i, line in enumerate(lines)
         if (m := KEY_LINE.match(line)) and m.group("key") == "title"),
        len(lines),
    )
    lines[position:position] = new_lines
    updated = opening + "".join(lines) + rest
    yaml.safe_load(split_front_matter(updated)[1])
    return updated


def rename_seo(text):
    """Return text with a legacy seo key renamed to seo_description."""
    parts = split_front_matter(text)
    if parts is None:
        return text
    opening, body, rest = parts
    data = yaml.safe_load(body) or {}
    if "seo" not in data or "seo_description" in data:
        return text
    lines = body.splitlines(keepends=True)
    for i, line in enumerate(lines):
        match = KEY_LINE.match(line)
        if match and match.group("key") == "seo":
            lines[i] = "seo_description" + line[match.end("key"):]
    return opening + "".join(lines) + rest


def is_indexable(path, data):
    if str(data.get("robots") or "").find("noindex") >= 0:
        return False
    # an explicit robots value overrides the collection default
    in_noindex_dir = path.relative_to(ROOT).parts[0] in NOINDEX_DIRS
    return not (in_noindex_dir and data.get("robots") is None)


def content_files(paths):
    for base in paths:
        base = (ROOT / base).resolve()
        files = [base] if base.is_file() else sorted(base.rglob("*"))
        for path in files:
            if path.suffix in (".md", ".html") and path.is_file():
                yield path


def audit(paths):
    """Print indexable files with missing or out of range seo values."""
    issues = 0
    for path in content_files(paths):
        parts = split_front_matter(path.read_text(encoding="utf-8"))
        if parts is None:
            continue
        data = yaml.safe_load(parts[1]) or {}
        if not is_indexable(path, data):
            continue
        title = str(data.get("seo_title") or "")
        description = str(data.get("seo_description") or "")
        problems = check_lengths(title, description)
        if problems:
            issues += 1
            print(f"{path.relative_to(ROOT)}: {'; '.join(problems)}")
    print(f"{issues} file(s) need attention")
    return issues


def apply(mapping_path):
    """Write seo values from a JSON mapping of path to title/description."""
    mapping = json.loads(pathlib.Path(mapping_path).read_text("utf-8"))
    failures = 0
    for relative, values in mapping.items():
        title = values["seo_title"].strip()
        description = values["seo_description"].strip()
        problems = check_lengths(title, description)
        if problems:
            failures += 1
            print(f"{relative}: {'; '.join(problems)}")
            continue
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        path.write_text(set_seo(text, title, description), encoding="utf-8")
    print(f"{len(mapping) - failures} updated, {failures} rejected")
    return failures


def migrate(paths):
    """Rename legacy seo keys to seo_description."""
    count = 0
    for path in content_files(paths):
        text = path.read_text(encoding="utf-8")
        updated = rename_seo(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            count += 1
    print(f"{count} file(s) migrated")


# processing
if __name__ == "__main__":
    arguments = argparse.ArgumentParser(
        description="""Manage seo_title and seo_description front matter.""")
    commands = arguments.add_subparsers(dest="command", required=True)

    audit_parser = commands.add_parser("audit", help="Report seo issues")
    audit_parser.add_argument("paths", nargs="*", default=CONTENT_DIRS)

    apply_parser = commands.add_parser("apply", help="Apply a JSON mapping")
    apply_parser.add_argument("mapping")

    migrate_parser = commands.add_parser("migrate",
                                         help="Rename seo to seo_description")
    migrate_parser.add_argument("paths", nargs="+")

    args = arguments.parse_args()
    if args.command == "audit":
        raise SystemExit(1 if audit(args.paths) else 0)
    if args.command == "apply":
        raise SystemExit(1 if apply(args.mapping) else 0)
    migrate(args.paths)
