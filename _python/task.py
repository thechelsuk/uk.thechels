# importing modules
import pathlib
import helper
import datetime


working_date = datetime.date.today()

string = ""

if helper.isGardenWasteDay(working_date):
    string += "- Garden Waste Day /n"
if helper.isRecyclingWasteDay(working_date):
    string += "- Recycling Waste Collection Day /n"
if helper.isRefuseWasteDay(working_date):
    string += "- Refuse Waste Collection Day /n"
if helper.isTuesday(working_date):
    string += "- Food Waste Collection Day /n"
if string == "":
    string = "No tasks today"

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        f = root / "_pages/morning.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "task_marker", string)
        f.open("w").write(c)
        print("Task completed")
    except FileNotFoundError:
        print('File does not exist, unable to proceed')