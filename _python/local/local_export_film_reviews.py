from __future__ import annotations

from datetime import datetime, timedelta
import os
from typing import Iterable, List, Tuple, Dict, Any

import pytz
import yaml

import config

Film = Dict[str, Any]
TimedFilm = Tuple[datetime, Film]


def load_films(yaml_file: str) -> List[Film]:
    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    if not isinstance(data, list):
        raise ValueError("YAML root must be a list of films")
    return data


def _ensure_aware_utc(dt: datetime) -> datetime:
    """Return a UTC, timezone‑aware datetime for comparison."""
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(pytz.UTC)


def _parse_film_date(raw: Any) -> datetime | None:
    """Parse the film date field into an aware UTC datetime, or None on failure."""
    if isinstance(raw, datetime):
        return _ensure_aware_utc(raw)

    if isinstance(raw, str):
        try:
            # Handle ISO8601 with optional trailing Z
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except Exception:
            return None
        return _ensure_aware_utc(dt)

    return None


def filter_recent_films(
    films: Iterable[Film],
    days: int = 30,
    today: datetime | None = None,
) -> List[TimedFilm]:
    if today is None:
        today = datetime.now().astimezone()
    today_utc = _ensure_aware_utc(today)
    start_date = today_utc - timedelta(days=days)

    recent: List[TimedFilm] = []

    for film in films:
        film_dt = _parse_film_date(film.get("date"))
        if film_dt is None:
            continue
        if start_date <= film_dt <= today_utc:
            recent.append((film_dt, film))

    recent.sort(key=lambda x: x[0])
    return recent


def build_post_content(
    recent_films: Iterable[TimedFilm],
    today: datetime | None = None,
) -> str:
    if today is None:
        today = datetime.now()

    post_time = today.strftime("%Y-%m-%d %H:%M")
    title_date = today.strftime("%B-%Y")

    front_matter = ("---\n"
                    "\n"
                    "layout: post\n"
                    f"date: {post_time}\n"
                    f"title: Film Monthly for {title_date}\n"
                    "syndicate: false\n"
                    "type: film\n"
                    "\n"
                    "---")

    content_lines = [""]  # ensures a newline after front matter
    for _, film in recent_films:
        title = film.get("title", "Unknown Title")
        year = film.get("year", "")
        rating = film.get("rating")
        rating_str = f"{rating}/10" if rating is not None else "N/A"
        content_lines.append(f"- {title} [{year}], rated {rating_str}")

    content = "\n".join(content_lines)
    return front_matter + content + "\n"


def build_output_path(today: datetime | None = None) -> str:
    # Workspace root: two levels up from this script (from _python/local/)
    workspace_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../.."))

    if today is None:
        today = datetime.now()

    post_date = today.strftime("%Y-%m-%d")
    post_year = today.strftime("%Y")
    file_date = today.strftime("%B-%Y").lower()

    post_filename = f"{post_date}-film-monthly-{file_date}.md"
    post_dir = os.path.join(workspace_root, "_posts", post_year)
    return os.path.join(post_dir, post_filename)


def process_yaml(yaml_file: str,
                 output_file: str,
                 today: datetime | None = None) -> None:
    if today is None:
        today = datetime.now()

    films = load_films(yaml_file)
    recent_films = filter_recent_films(films, days=30, today=today)

    if not recent_films:
        print("No films found in the last 30 days.")
        return

    content = build_post_content(recent_films, today=today)

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(content)

    print(f"Blog post created: {output_file}")


if __name__ == "__main__":
    yaml_path = config.FILM_YML
    out_path = build_output_path()
    process_yaml(yaml_path, out_path)
