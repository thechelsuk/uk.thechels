# importing modules
import json
import re
import feedparser
from yahoo_fin import stock_info as si

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)


# Methods
def remove_img_tags(data):
    p = re.compile(r'<img.*?/>')
    return p.sub('', data)


def ord(n):
    return str(n)+("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def dtStylish(dt,f):
    return dt.strftime(f).replace("{th}", ord(dt.day))


def pprint(string):
    json_formatted_str = json.dumps(string, indent=2)
    print(json_formatted_str)

def fetch_cfc_entries(url):
    entries = feedparser.parse(url)["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]

def get_stocks(set_of_tickers):
    string_builder = ""
    for ticker in list(set_of_tickers):
        string_builder += f"<li>{ticker} : {round(si.get_live_price(ticker),5)}</li>\n"
    return string_builder