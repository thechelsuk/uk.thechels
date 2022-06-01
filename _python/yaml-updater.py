# importing modules
import os
import pathlib

root = pathlib.Path(__file__).parent.parent.resolve()
c = os.getenv("content").replace('`','').strip()
l = os.getenv("label").strip()
p = root / f"_data/{l}.yml"
try:
    with open(p, 'a') as f:
        o = f.write(f"- {c}")
        print(f"{l} completed\n{o}")
except FileNotFoundError:
        print('File does not exist, unable to proceed')