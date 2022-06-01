# importing modules
from datetime import datetime
import json
import re
import feedparser
from yahoo_fin import stock_info as si


def replace_chunk(content: str, marker: str, chunk: str) -> str:
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)


def remove_img_tags(data: str) -> str:
    p = re.compile(r'<img.*?/>')
    return p.sub('', data)


def ord(n: int) -> str:
    return str(n)+("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def dtStylish(dt,f):
    return dt.strftime(f).replace("{th}", ord(dt.day))


def pprint(string: str) -> str:
    json_formatted_str = json.dumps(string, indent=2)
    print(json_formatted_str)


def fetch_cfc_entries(url: str) -> list:
    entries = feedparser.parse(url)["entries"]
    return [
        {
            "title": entry["description"],
            "url": entry["link"].split("#")[0],
            "published": convert_cfc_date(entry["published"]),
        }
        for entry in entries
    ]

def convert_cfc_date(input: str) -> str:
    working =  datetime.strptime(input, "%a, %d %b %Y %H:%M:%S %z")
    output = datetime.strftime(working, "%d %b")
    return output


def get_stocks(set_of_tickers: str) -> str:
    markdown = ""
    for ticker in list(set_of_tickers):
        markdown += f"- {ticker} : {round(si.get_live_price(ticker),5)}\n"
    return markdown
