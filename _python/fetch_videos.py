import argparse
import pathlib
import os
import datetime
import re
import hashlib
import feedparser
import yaml
import seo_frontmatter

ROOT = pathlib.Path(__file__).parent.parent.resolve()
RSS_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCwK4oZ8hw9RS6tZKEjw_qLw"
OUTPUT_FOLDER = ROOT / "_posts"

# ================= HELPER FUNCTIONS =================


def get_video_id(entry):
    """
    Extracts the video ID from the XML custom element yt:videoId.
    Returns just the video ID (e.g. '9l1GQ7fQwIg').
    """
    # Primary source: <yt:videoId>, which feedparser exposes as yt_videoid
    video_id = entry.get('yt_videoid') or entry.get('yt:videoId')

    if video_id:
        return video_id.strip()

    # Fallback to link parsing only if custom ID is missing
    link = entry.get('link')
    if link:
        # Handle standard YouTube format
        video_id = extract_id_from_link(link)
        if video_id:
            return video_id
    return None


def extract_id_from_link(link):
    """
    Safely extracts the video ID from various YouTube URL formats.
    Returns None if extraction fails.
    """
    # Standard watch URL
    parts = link.split('v=')
    if len(parts) > 1:
        # Get the string after v=
        video_id = parts[1].split('&')[0].split('?')[0]
        # Remove any trailing chars (like t for YouTube short)
        video_id = re.sub(r'[^a-zA-Z0-9_-]', '', video_id)
        if len(video_id) == 11:
            return video_id

    # Shorts URL format (e.g., youtube.com/shorts/sQtW_IPB-Yk)
    if '/shorts/' in link:
        parts = link.split('/shorts/')
        if len(parts) > 1:
            video_id = parts[1].split('/')[0]
            video_id = re.sub(r'[^a-zA-Z0-9_-]', '', video_id)
            if len(video_id) == 11:
                return video_id

    # Watch URL alternative (e.g., youtube.com/watch?v=...)
    if 'watch' in link and 'shorts' not in link:
        parts = link.split('watch')
        if len(parts) > 1:
            parts = parts[1].split('v=')
            if len(parts) > 1:
                video_id = parts[1].split('&')[0]
                video_id = re.sub(r'[^a-zA-Z0-9_-]', '', video_id)
                if len(video_id) == 11:
                    return video_id

    return None


def parse_date(entry):
    """
    Parses the date from RSS entry.
    Returns a string in 'yyyy-mm-dd' format only (no time).
    Handles both str and datetime objects.
    """
    pub_date = entry.published

    # feedparser returns datetime object or ISO8601 string
    if isinstance(pub_date, str):
        try:
            # Handle timezone formats correctly
            dt = datetime.datetime.fromisoformat(
                pub_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    elif hasattr(pub_date, 'strftime'):
        dt = pub_date
    else:
        dt = datetime.datetime.now()

    # Format: 'yyyy-mm-dd' only (no time)
    return dt.strftime('%Y-%m-%d')


def get_year(date_str):
    """
    Extracts the year for the folder path.
    """
    if date_str and len(date_str) > 4:
        return date_str[:4]
    else:
        return datetime.datetime.now().strftime('%Y')


def clean_title_for_file(title):
    """
    Removes special characters to create a valid Markdown filename.
    Replaces spaces with hyphens.
    """
    # Remove anything that isn't alphanumeric or space/hyphen
    title = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    return title.lower().replace(' ', '-')


def get_unique_filename(year, date_str, title, video_id):
    """
    Generates the filename with the hash to prevent duplicates.
    Format: year/yyyymmdd-title-hash.md

    Folder: _posts/2025/
    Filename: 2025-04-18-shortkeys-title-hash.md
    """
    clean_title_for_filename = clean_title_for_file(title)

    # Hash the video ID to ensure uniqueness even if title changes
    video_id_hash = get_video_id_hash(video_id)

    # Filename: yyyy-mm-dd-title-hash.md
    filename = f"{date_str}-video-{clean_title_for_filename}-{video_id_hash}.md"
    return f"{year}/{filename}"


def get_video_id_hash(video_id):
    """Returns the filename-safe identifier derived from a video ID."""
    return hashlib.sha256(video_id.encode()).hexdigest()[:8]


def is_short(entry):
    """True for YouTube Shorts (portrait videos)."""
    return '/shorts/' in (entry.get('link') or '')


def get_thumbnail(entry):
    """Thumbnail URL from the feed, else YouTube's standard one for the ID."""
    thumbnails = entry.get('media_thumbnail') or []
    if thumbnails and thumbnails[0].get('url'):
        return thumbnails[0]['url']
    video_id = get_video_id(entry)
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else None


TRAILING_HASHTAGS = re.compile(r"(?:[\s,]*#\w+)+[\s,]*$")
HASHTAG = re.compile(r"(?<![\w/])#(\w+)")
HASHTAG_LINE = re.compile(r"^(?:#\w+[\s,]*)+$")

LINKING_WORDS = {
    "on", "in", "at", "by", "for", "with", "from", "to", "of", "and", "via",
    "about"
}


def clean_title(title):
    """
    Removes hashtags from a video title: a trailing run of them is dropped
    ("Fractions #shorts" -> "Fractions"), unless it follows a linking word,
    when the first one keeps its word ("on #Twitch" -> "on Twitch"). One
    inside the title keeps its word ("#thechelsuk on" -> "thechelsuk on").
    """
    title = title or ""
    trailing = TRAILING_HASHTAGS.search(title)
    if trailing:
        head = title[:trailing.start()]
        words = head.split()
        tags = re.findall(r"#(\w+)", trailing.group(0))
        if words and words[-1].lower() in LINKING_WORDS:
            head = f"{head} {tags[0]}"
        title = head
    title = HASHTAG.sub(r"\1", title)
    return re.sub(r"\s+", " ", title).strip(" ,|-:")


URL_PATTERN = re.compile(r"(?<![<(])(https?://[^\s<>]*[^\s<>.,;:!?)\]])")


def description_to_markdown(description):
    """
    Turns a plain-text YouTube description into Markdown: paragraphs kept,
    single line breaks kept as hard breaks, bare URLs made into links and
    leading hashtags escaped so they don't become headings.
    """
    if not description or not description.strip():
        return ""

    text = description.replace('\r\n', '\n').strip()
    paragraphs = []
    for block in re.split(r"\n\s*\n", text):
        lines = []
        for line in block.split('\n'):
            line = line.strip()
            if not line or HASHTAG_LINE.match(line):
                continue
            if line.startswith('#'):
                line = '\\' + line
            lines.append(URL_PATTERN.sub(r"<\1>", line))
        if lines:
            paragraphs.append("  \n".join(lines))
    return "\n\n".join(paragraphs)


def post_exists_for_video(video_id):
    """Checks every generated post, regardless of its date or title."""
    video_id_hash = get_video_id_hash(video_id)
    filename_suffix = f"-{video_id_hash}.md"

    return any(
        path.name.endswith(filename_suffix)
        for path in OUTPUT_FOLDER.rglob("*.md"))


VIDEO_SEO_PADDING = ("Watch it on YouTube through the link in this post. "
                     "Browse my other videos, shorts and app demos. "
                     "New videos are posted here as they go live.")


def seo_fields(title):
    """Generated seo_title and seo_description for a video title."""
    seo_title = seo_frontmatter.fit_title(f"{title} - Video")
    seo_description = seo_frontmatter.fit_description(
        f"A video from my YouTube channel: {title}.", VIDEO_SEO_PADDING)
    return seo_title, seo_description


TITLE_FIELD = re.compile(r"^(title|seo_title|seo_description):[ \t]*(.+)$",
                         re.M)


def clean_title_fields(text):
    """
    Cleans hashtags out of an existing post's title. seo_title and
    seo_description are regenerated when they were generated from the old
    title or contain a hashtag; hand-written ones are kept. Returns the new
    text, or None if the title is already clean.
    """
    parts = seo_frontmatter.split_front_matter(text)
    if not parts:
        return None
    opening, fm, rest = parts
    fields = {m.group(1): m.group(2) for m in TITLE_FIELD.finditer(fm)}
    if "#" not in fields.get("title", ""):
        return None
    old_title = yaml.safe_load(fields["title"])
    title = clean_title(old_title)
    new_values = {"title": title}
    # Regenerate seo fields that were generated from the old title (or still
    # have a hashtag); hand-written ones are kept.
    for key, old_generated, generated in zip(("seo_title", "seo_description"),
                                             seo_fields(old_title),
                                             seo_fields(title)):
        value = fields.get(key)
        if value is None:
            continue
        value = yaml.safe_load(value)
        if "#" in value or value == old_generated:
            new_values[key] = generated

    def replace(match):
        key = match.group(1)
        if key not in new_values:
            return match.group(0)
        return f"{key}: {seo_frontmatter.quote(new_values[key])}"

    return opening + TITLE_FIELD.sub(replace, fm) + rest


def video_front_matter(entry):
    """The video-only front matter lines: ID, Short flag and thumbnail."""
    lines = [
        f"video_id: {seo_frontmatter.quote(get_video_id(entry) or '')}",
        f"short: {'true' if is_short(entry) else 'false'}"
    ]
    thumbnail = get_thumbnail(entry)
    if thumbnail:
        lines.append(f"image: {seo_frontmatter.quote(thumbnail)}")
    return "\n".join(lines) + "\n"


def create_front_matter(entry):
    """
    Generates the Front Matter YAML.
    Includes: layout, title, seo fields, date, source, type, and the video
    ID, Short flag and thumbnail (used for the player and share image).
    NO author, NO tags, NO categories, NO permalink.
    """
    title = clean_title(entry.title)
    link = entry.link
    video_id = get_video_id(entry)

    # Parse date for display
    date_str = parse_date(entry)
    year_folder = get_year(date_str)

    seo_title, seo_description = seo_fields(title)

    # Construct Front Matter
    fm_content = f"""---
title: {seo_frontmatter.quote(title)}
seo_title: {seo_frontmatter.quote(seo_title)}
seo_description: {seo_frontmatter.quote(seo_description)}
date: "{date_str}"
layout: post
source: {seo_frontmatter.quote(link)}
type: video
{video_front_matter(entry)}---
"""

    return fm_content


def generate_body(entry):
    """
    Generates the Markdown body: the video description (if any), then a
    link to watch on YouTube. The player itself comes from the post layout.
    """
    link = f"[Watch on YouTube]({entry.get('link')})\n"
    description = description_to_markdown(entry.get('summary'))
    return f"{description}\n\n{link}" if description else link


THIN_BODY = re.compile(r"\A\s*\[Watch on Youtube\]\([^)]*\)\s*\Z", re.I)


def backfill_post(text, entry):
    """
    Upgrades an existing post that is still just the watch link: adds the
    video front matter and the description. Returns the new text, or None
    when the post already has its details or has its own words.
    """
    parts = seo_frontmatter.split_front_matter(text)
    if not parts:
        return None
    opening, fm, rest = parts
    if re.search(r"^video_id:", fm, re.M):
        return None
    body = rest.split("\n", 1)[1] if "\n" in rest else ""
    if not THIN_BODY.match(body):
        return None
    closing = rest.split("\n", 1)[0] + "\n"
    return opening + fm + video_front_matter(
        entry) + closing + "\n" + generate_body(entry)


def backfill_existing(entries):
    """Runs backfill_post over existing posts for the videos in the feed."""
    by_hash = {
        get_video_id_hash(get_video_id(e)): e
        for e in entries if get_video_id(e)
    }
    updated = 0
    for path in OUTPUT_FOLDER.rglob("*-video-*.md"):
        text = path.read_text(encoding="utf-8")
        new_text = clean_title_fields(text) or text
        entry = by_hash.get(path.stem.rsplit("-", 1)[-1])
        if entry:
            new_text = backfill_post(new_text, entry) or new_text
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"✓ Backfilled: {path.name}")
    print(f"Backfilled {updated} post(s).")


def save_post_to_jekyll(fm_content, body_content, filename, video_id=None):
    """
    Writes the file to the correct directory structure.
    """
    file_content = fm_content + body_content

    # Construct file path inside _posts folder
    file_path = os.path.join(OUTPUT_FOLDER, filename)

    if os.path.exists(file_path) or (video_id
                                     and post_exists_for_video(video_id)):
        print(f"✓ Skipping existing file: {file_path}")
        return

    # Ensure parent directories exist (e.g. _posts/2025)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
    except Exception as e:
        print(f"x Failed to write file {file_path}: {e}")


def process_entry(entry):
    """
    Pure function. Handles the logic for one entry.
    This is what you can test locally with mock entries.
    """
    title = clean_title(entry.title)
    link = entry.link
    video_id = get_video_id(entry)

    fm_content = create_front_matter(entry)
    body_content = generate_body(entry)
    filename = get_unique_filename(get_year(parse_date(entry)),
                                   parse_date(entry), title, video_id)

    return fm_content, body_content, filename


def run_main(backfill=False):
    """
    Main entry point.
    Parses RSS and writes files. With backfill, also upgrades existing
    link-only posts for videos still in the feed.
    """
    # Parse feed entries
    feed = feedparser.parse(RSS_FEED_URL)
    entries = feed.entries

    if not entries:
        print("No entries found in RSS feed.")
        return

    if backfill:
        backfill_existing(entries)

    print(f"Found {len(entries)} videos to process.")

    for entry in entries:
        try:
            # Process content
            fm, body, filename = process_entry(entry)

            # Save file
            save_post_to_jekyll(fm, body, filename, get_video_id(entry))

        except Exception as e:
            # Only print the error message, not the entire entry
            error_msg = str(e)
            print(f"x Error processing entry: {error_msg}")
            continue

    print("Script finished.")


# ================= MAIN EXECUTION =================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch YouTube videos as posts.")
    parser.add_argument(
        "--backfill",
        action="store_true",
        help=
        "also add descriptions and video details to existing link-only posts")
    run_main(parser.parse_args().backfill)
