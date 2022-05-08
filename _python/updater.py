# importing modules
import json
import os
import pathlib

filename = os.getenv("label")
content = os.getenv("content")

root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / f"_data/{filename}.json", 'r+') as filehandle:
    data = json.load(filehandle)
    data.append(f"{content.rstrip()}")
    filehandle.seek(0)
    json.dump(data, filehandle, indent=4)
