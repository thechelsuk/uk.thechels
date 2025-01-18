# importing modules
import json
import os
import pathlib
from datetime import date

import helper
import requests

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        LAT = os.getenv("lat")
        LON = os.getenv("lon")
        APIKEY = os.getenv("open_weather_key")
        url = (
            "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%"
            "s&appid=%s&exclude=current,minutely,hourly,alerts&units=metric" %
            (LAT, LON, APIKEY))

        response = requests.get(url)
        response_dict = json.loads(response.text)
        d = date.today()
        output_date = d.strftime("%A, %d %B %Y")

        avg_temp = str(response_dict["main"]["temp"])
        feels_like = str(response_dict["main"]["feels_like"])
        today_desc = str(response_dict["weather"][0]["description"])

        string_today = f"### Daily Rundown on {output_date}\n\n"
        string_today += f"- The average temperature today is {avg_temp}˚C;\n"
        string_today += f"- but will feel like {feels_like}˚C"
        string_today += f"- You can expect a {today_desc} outlook for the day.\n"

        print(string_today)

        f = root / "_pages/morning.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "weather_marker", string_today)
        f.open("w").write(c)
        print("Weather completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
