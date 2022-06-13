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
    """Injects content into a template marker"""
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)


def remove_img_tags(data: str) -> str:
    """Removes img tags from a string"""
    p = re.compile(r"<img.*?/>")
    return p.sub("", data)


def get_ordinal_string(n: int) -> str:
    """Returns the ordinal of a number"""
    return str(n) + (
        "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    )


def stylish_datetime(dt, f):
    """Returns a more stylish datetime format"""
    return dt.strftime(f).replace("{th}", get_ordinal_string(dt.day))


def pretty_print(string: str) -> str:
    """Pretty prints a string"""
    json_formatted_str = json.dumps(string, indent=2)
    return json_formatted_str


def fetch_cfc_entries(url: str) -> list:
    """Fetches CFC entries from a given url"""
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
    """Converts CFC's standard date format to a more readable format"""
    working = datetime.strptime(input, "%a, %d %b %Y %H:%M:%S %z")
    output = datetime.strftime(working, "%d %b")
    return output


def get_stocks(set_of_tickers: list) -> str:
    """Returns a string of stock prices for a given set of tickers"""
    markdown = ""
    for ticker in list(set_of_tickers):
        markdown += f"- {ticker} : {round(si.get_live_price(ticker),5)}\n"
    return markdown


def get_day_of_the_week(today: datetime) -> str:
    """Returns the day of the week"""
    return today.strftime("%A")


def get_week_number(value: datetime) -> int:
    """Returns the week number of a given date"""
    return value.isocalendar()[1]


def is_odd_number(number: int) -> bool:
    """Returns true if a number is odd"""
    if number % 2 == 0:
        return False
    return True


def is_week_one(week: int) -> bool:
    """Returns true if a number is odd"""
    if is_odd_number(week):
        return True
    return False


def is_week_two(week: int) -> bool:
    """Returns true if a number is even"""
    if is_odd_number(week):
        return False
    return True


def is_monday(today) -> bool:
    """Returns true if a date is Monday"""
    return get_day_of_the_week(today) == "Monday"


def is_tuesday(today) -> bool:
    """Returns true if a date is Tuesday"""
    return get_day_of_the_week(today) == "Tuesday"


def is_garden_waste_day(today) -> bool:
    """Returns true if a date is Tuesday and is week two"""
    if is_monday(today) and is_week_two(get_week_number(today)):
        return True
    return False


def is_recycling_waste_day(today) -> bool:
    """Returns true if a date is Tuesday and is week one"""
    if is_tuesday(today) and is_week_one(get_week_number(today)):
        return True
    return False


def is_refuse_waste_day(today) -> bool:
    """Returns true if a date is Tuesday and is week two"""
    if is_tuesday(today) and is_week_two(get_week_number(today)):
        return True
    return False


def create_date(input: str) -> datetime:
    """Returns a datetime object from a string"""
    return datetime.strptime(input, "%Y-%m-%d")


def get_corona(records: int) -> str:
    """Returns a string of corona records from hardcoded url"""
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
    """Returns a string of random items from a list"""
    for item in random.sample(items, counter):
        string += f"- {item}\n"
    return string
