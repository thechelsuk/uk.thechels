# importing modules
import requests
import json
import re
from datetime import datetime

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
    working =  datetime.strptime(input, "%a, %d %b %Y %H:%M:%S %z")
    output = datetime.strftime(working, "%d %b")
    return output


def get_stocks(set_of_tickers: list) -> str:
    markdown = ""
    for ticker in list(set_of_tickers):
        markdown += f"- {ticker} : {round(si.get_live_price(ticker),5)}\n"
    return markdown

def getDayOfTheWeek(today: datetime) -> str:
    return today.strftime("%A")

def getWeekNumber(value: datetime) -> int:
    return value.isocalendar()[1]

def isOddNumber(number: int) -> bool:
    if number % 2 == 0:
        return False
    return True

def ifWeekOne(week: int) -> bool:
    if isOddNumber(week):
        return True
    return False

def ifWeekTwo(week: int) -> bool:
    if isOddNumber(week):
        return False
    return True

def isMonday(today) -> bool:
    return getDayOfTheWeek(today) == "Monday"

def isTuesday(today) -> bool:
    return getDayOfTheWeek(today) == "Tuesday"

def isGardenWasteDay(today) -> bool:
    if isMonday(today) and ifWeekTwo(getWeekNumber(today)):
        return True
    return False

def isRecyclingWasteDay(today) -> bool:
    if isTuesday(today) and ifWeekOne(getWeekNumber(today)):
        return True
    return False

def isRefuseWasteDay(today) -> bool:
    if isTuesday(today) and ifWeekTwo(getWeekNumber(today)):
        return True
    return False

def createDate(input: str) -> datetime:
    return datetime.strptime(input, "%Y-%m-%d")

def get_corona(records: int) -> str:
    url = "https://raw.githubusercontent.com/Cheltenham-Open-Data/covid/main/corona.json"
    response = requests.get(url).json()
    data = response["body"]
    string_builder = f"Last {records} days\n\n"
    for i in range(0, records):
        string_builder += (f"- {0 if data[i]['newCasesByPublishDate'] == None else data[i]['newCasesByPublishDate']} new cases & "
        f"{0 if data[i]['newDeaths28DaysByPublishDate'] == None else data[i]['newDeaths28DaysByPublishDate']} deaths on {data[i]['date']}\n")
    return string_builder