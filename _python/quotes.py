# importing modules
import helper
import random
import pathlib
import json

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "_data/quotes.json", 'r') as filehandle:
    random_quote = random.choice(json.load(filehandle))

# processing
if __name__ == "__main__":
    p = root / "morning.html"
    c = p.open().read()
    f = helper.replace_chunk( c, "quote_marker", f'<p class="quote">{random_quote}</p>')
    p.open("w").write(f)

print('Quotes Completed')
