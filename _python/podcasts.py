# import modules
import os
import pathlib

# processing
try:
    root = pathlib.Path(__file__).parent.parent.resolve()
    yamlFile = root / "_data/podcasts.yml"
    content = os.getenv("content").replace("`", "").strip()
    with open(yamlFile, "a") as f:
        outputs = f.write("/n" + content)
    print("Podcasts completed")

except FileNotFoundError:
    print("File does not exist, unable to proceed")
