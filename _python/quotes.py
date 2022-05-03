# importing modules
import helper
import random
import pathlib
import json

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "_config/quotes.json", 'r') as filehandle:
    random_quote = random.choice(json.load(filehandle))
    random_quote = random_quote.replace( "-", "\n\n -")

# processing
if __name__ == "__main__":
    p = root / "morning.md"
    c = p.open().read()
    f = helper.replace_chunk( c, "quote_marker", f"> {random_quote}")
    p.open("w").write(f)

print('Quotes Completed')
