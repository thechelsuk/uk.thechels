# import modules
import datetime
import pathlib

import helper

# processing
if __name__ == "__main__":
    try:
        working_date = datetime.date.today()
        string = ""
        if helper.is_garden_waste_day(working_date):
            string += "- Garden Waste Day\n"
        if helper.is_recycling_waste_day(working_date):
            string += "- Recycling Waste Collection Day\n"
        if helper.is_refuse_waste_day(working_date):
            string += "- Refuse Waste Collection Day\n"
        if helper.is_tuesday(working_date):
            string += "- Food Waste Collection Day\n"
        if helper.is_water_the_plants_day(working_date):
            string += "- Water the plants\n"
        if helper.is_farmers_marker(working_date):
            string += "- Farmers Market in town\n"
        if string == "":
            string = "- No tasks today"
        root = pathlib.Path(__file__).parent.parent.resolve()
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "task_marker", string)
        f.open("w").write(c)
        print("Task completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
