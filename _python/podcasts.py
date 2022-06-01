# importing modules
import os
import pathlib
from turtle import onclick

root = pathlib.Path(__file__).parent.parent.resolve()
p = root / "_data/podcasts.yml"
c = os.getenv("content").replace('`','').strip()

try:
    with open(p, 'a') as f:
        o = f.write(c)
        print(f"Podcast completed\n{o}")
except FileNotFoundError:
        print('File does not exist, unable to proceed')
