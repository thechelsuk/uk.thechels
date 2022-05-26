# importing modules
import json
import os
import pathlib

filename = os.getenv("label")
content = os.getenv("content")
root = pathlib.Path(__file__).parent.parent.resolve()

try:    
    with open( root / f"_data/{filename}.json", 'r+') as f:
        data = json.load(f)
        data.append(f"{content.rstrip()}")
        f.seek(0)
        json.dump(data, f, indent=4)
except FileNotFoundError:
        print('File does not exist, unable to proceed') 
