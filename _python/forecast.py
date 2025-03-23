# importing modules
import json
import os
import pathlib
from datetime import date, datetime

import helper
import requests


# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        APIKEY = os.getenv("OPEN_WEATHER_KEY") or ''
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        url = f"{BASE_URL}?q=Cheltenham&appid={APIKEY}&units=metric"

        response = requests.get(url)
        response_dict = json.loads(response.text)

        if response_dict["cod"] != 200:
            string_today = "- Weather data not available"
        else:
            output_date = datetime.date.today().strftime("%A, %d %B %Y")

            day_temp = str(response_dict["main"]["temp"])
            feels_like = str(response_dict["main"]["feels_like"])
            day_desc = str(response_dict["weather"][0]["description"])
            high_temp = str(response_dict["main"]["temp_max"])
            low_temp = str(response_dict["main"]["temp_min"])
            wind_speed = str(response_dict["wind"]["speed"])
            visibility = str(response_dict["visibility"])
            pressure = str(response_dict["main"]["pressure"])
            humidity = str(response_dict["main"]["humidity"])

            sunrise = datetime.datetime.fromtimestamp(response_dict["sys"]["sunrise"]).strftime("%H:%M")
            sunset = datetime.datetime.fromtimestamp(response_dict["sys"]["sunset"]).strftime("%H:%M")

            string_today = f"## On {output_date}\n\n"
            string_today += f"- The average temperature today is {day_temp}˚C,\n"
            string_today += f"- With highs of {high_temp}˚C and lows of {low_temp}˚C,\n"
            string_today += f"- It may feel like {feels_like}˚C with {day_desc}\n"
            string_today += f"- The wind speed is {wind_speed}m/s and visibility is {visibility}m\n"
            string_today += f"- The pressure is {pressure}hPa and humidity is {humidity}%\n"
            string_today += f"- The sun will rise at {sunrise} and set at {sunset}\n"

        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "weather_marker", string_today)
        f.open("w").write(c)
        print("Weather completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
