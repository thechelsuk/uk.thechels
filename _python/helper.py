# importing modules
import json
import random
import re
from datetime import datetime

import feedparser
import requests
from yahoo_fin import stock_info as si


# methods
def replace_chunk(content: str, marker: str, chunk: str) -> str:
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)


def remove_img_tags(data: str) -> str:
    p = re.compile(r"<img.*?/>")
    return p.sub("", data)


def ord(n: int) -> str:
    return str(n) + (
        "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    )


def dtStylish(dt, f):
    return dt.strftime(f).replace("{th}", ord(dt.day))


def pprint(string: str) -> str:
    json_formatted_str = json.dumps(string, indent=2)
    return json_formatted_str


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
    working = datetime.strptime(input, "%a, %d %b %Y %H:%M:%S %z")
    output = datetime.strftime(working, "%d %b")
    return output


def get_stocks(set_of_tickers: list) -> str:
    markdown = ""
    for ticker in list(set_of_tickers):
        markdown += f"- {ticker} : {round(si.get_live_price(ticker),5)}\n"
    return markdown


def get_day_of_the_week(today: datetime) -> str:
    return today.strftime("%A")


def get_week_number(value: datetime) -> int:
    return value.isocalendar()[1]


def is_odd_number(number: int) -> bool:
    if number % 2 == 0:
        return False
    return True


def is_week_one(week: int) -> bool:
    if is_odd_number(week):
        return True
    return False


def is_week_two(week: int) -> bool:
    if is_odd_number(week):
        return False
    return True


def is_monday(today) -> bool:
    return get_day_of_the_week(today) == "Monday"


def is_tuesday(today) -> bool:
    return get_day_of_the_week(today) == "Tuesday"


def is_garden_waste_day(today) -> bool:
    if is_monday(today) and is_week_two(get_week_number(today)):
        return True
    return False


def is_recycling_waste_day(today) -> bool:
    if is_tuesday(today) and is_week_one(get_week_number(today)):
        return True
    return False


def is_refuse_waste_day(today) -> bool:
    if is_tuesday(today) and is_week_two(get_week_number(today)):
        return True
    return False


def create_date(input: str) -> datetime:
    return datetime.strptime(input, "%Y-%m-%d")


def get_corona(records: int) -> str:
    url = (
        "https://raw.githubusercontent.com/Cheltenham-Open-Data/covid/main/corona.json"
    )
    response = requests.get(url).json()
    data = response["body"]
    string_builder = f"##### Latest {records} day Local Corona Data\n\n"
    for i in range(0, records):
        string_builder += (
            f"- {data[i]['newCasesByPublishDate']} new cases & "
            f"{data[i]['newDeaths28DaysByPublishDate']} deaths on {data[i]['date']}\n"
        )
    return string_builder


def get_random_items_from_a_list(string: str, items: list, counter: int) -> str:
    for item in random.sample(items, counter):
        string += f"- {item}\n"
    return string
