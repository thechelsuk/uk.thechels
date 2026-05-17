from io import BytesIO
import pathlib
import requests
import os
import argparse
import html
import re
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urljoin, quote_plus, urlparse, parse_qs
from PIL import Image
from ruamel.yaml import YAML

OUTPUT_FILE = "./_data/read.yml"
yaml = YAML()
yaml.default_flow_style = False


def load_book_file(file_path):
    path = pathlib.Path(file_path)
    if not path.exists():
        return []
    with path.open("r") as f:
        data = yaml.load(f)
        return data if isinstance(data, list) else []


def save_books(file_path, books):
    with pathlib.Path(file_path).open("w") as f:
        yaml.dump(books, f)


def add_book_to_list(book_data):
    library_books = load_book_file(OUTPUT_FILE)
    isbn = book_data["isbn"]
    if isinstance(isbn, list):
        isbn = isbn[0]
    for book in library_books:
        if book["isbn"] == isbn:
            return False
    library_books.append(book_data)
    save_books(OUTPUT_FILE, library_books)
    return True


def search_isbnsearch_org(query):
    """
    Search isbnsearch.org for the query (title, author, or ISBN) and parse the top results.
    Returns a list of dicts: {title, author, isbn, cover}
    """
    url = f"https://isbnsearch.org/search?s={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; add_book.py/1.0)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except Exception as exc:
        print(f"Error searching isbnsearch.org: {exc}")
        return []
    if resp.status_code != 200 or not resp.text:
        print(f"isbnsearch.org search failed: {resp.status_code}")
        return []
    html = resp.text
    results = []
    list_start = html.find('<ul id="searchresults">')
    if list_start == -1:
        return results
    list_end = html.find("</ul>", list_start)
    if list_end == -1:
        return results
    list_html = html[list_start:list_end + 5]
    item_matches = re.findall(r'<li>[\s\S]*?</li>', list_html, re.IGNORECASE)
    for li in item_matches[:5]:
        cover_match = re.search(r'<img[^>]+src="([^"]+)"', li, re.IGNORECASE)
        cover = cover_match.group(1).strip() if cover_match else ""
        title_match = re.search(r'<h2>\s*<a[^>]*>([^<]+)</a>\s*</h2>', li,
                                re.IGNORECASE)
        title = title_match.group(
            1).strip() if title_match else "Unknown Title"
        author_match = re.search(r'<p>\s*Author:\s*([^<]+)</p>', li,
                                 re.IGNORECASE)
        author = author_match.group(
            1).strip() if author_match else "Unknown Author"
        isbn_match = re.search(r'<p>\s*ISBN-13:\s*([0-9Xx-]+)</p>', li,
                               re.IGNORECASE)
        if not isbn_match:
            isbn_match = re.search(r'<p>\s*ISBN-10:\s*([0-9Xx-]+)</p>', li,
                                   re.IGNORECASE)
        isbn = isbn_match.group(1).strip() if isbn_match else ""
        if title and isbn:
            results.append({
                "title": title,
                "author": author,
                "isbn": isbn,
                "cover": cover
            })
    return results


def get_book_data(query):
    """
    Search isbnsearch.org for the query (ISBN, title, or author) and return the first result as book_data dict.
    """
    results = search_isbnsearch_org(query)
    if not results:
        print(f"No results found for '{query}' on isbnsearch.org.")
        return None
    book = results[0]
    book_data = {
        "isbn": book["isbn"],
        "dateFinished": date.today().isoformat(),
        "title": book["title"],
        "author": book["author"],
        "cover": book["cover"],
        "notes": "",
    }
    return book_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a book to the library.")
    parser.add_argument("--isbn",
                        required=True,
                        help="The ISBN, title, or search query for the book.")

    args = parser.parse_args()

    saved_book = get_book_data(args.isbn)
    if saved_book:
        if add_book_to_list(saved_book):
            # Download and save the cover image locally if available
            cover_url = saved_book.get("cover")
            if cover_url:
                try:
                    response = requests.get(cover_url, timeout=15)
                    if response.status_code == 200 and response.headers.get(
                            "Content-Type", "").startswith("image/"):
                        img = Image.open(BytesIO(response.content))
                        img.load()
                        width = 128
                        if img.width != width:
                            height = max(1,
                                         int(img.height * width / img.width))
                            img = img.resize((width, height), Image.LANCZOS)
                        new_cover_path = f"./image/books/book-{saved_book['isbn'].replace('-', '').replace(' ', '')}.png"
                        os.makedirs(os.path.dirname(new_cover_path),
                                    exist_ok=True)
                        img.convert("RGBA").save(new_cover_path, "PNG")
                        print(
                            f"Cover image saved to {new_cover_path} ({width}px wide PNG) from {cover_url}"
                        )
                        saved_book["cover"] = cover_url
                    else:
                        print(
                            f"Cover image not available or not an image: {cover_url}"
                        )
                except Exception as exc:
                    print(f"Failed to download or save cover image: {exc}")
        else:
            print("Book already exists in the list.")
    else:
        print("Book not found.")
