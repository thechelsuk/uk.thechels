# import modules
import pathlib
import helper
import yaml

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        with open(root / "_data/quotes.yml", "r") as stream:
            quote_list = yaml.load(stream, Loader=yaml.FullLoader)
        f = root / "_pages/daily.md"
        m = f.open().read()
        s = helper.get_random_quote_from_a_list("> ", quote_list, 1)
        c = helper.replace_chunk(m, "quote_marker", f"\n{s}")
        f.open("w").write(c)
        print("Quote Completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")