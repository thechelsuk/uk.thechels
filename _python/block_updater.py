# import modules
import os
import pathlib

# processing
try:
    label = os.getenv("label")
    content = os.getenv("content")
    content = content.replace("```yaml", "")
    content = content.replace("`", "").strip()
    root = pathlib.Path(__file__).parent.parent.resolve()
    yaml_file = root / "_data/{label}.yml"
    with open(yaml_file, "a") as f:
        outputs = f.write("/n" + content)
    print(f"{label} completed")

except FileNotFoundError:
    print(f"File does not exist for matching label {label}, unable to proceed")
