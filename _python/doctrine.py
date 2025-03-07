import requests
import pathlib
import helper
import yaml
import random
import os

FILE = "./_data/doctrine.yml"

if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        doctrine = root / FILE
        with doctrine.open() as f:
            items = yaml.safe_load(f)
        # Select a random film
        item = random.choice(items)
        string = f"- {item}"

        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "doctrine_marker", string)
        f.open("w").write(c)
        print("Doctrine completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
