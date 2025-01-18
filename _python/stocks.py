# import modules
import pathlib
import helper
import yaml

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        with open(root / "_data/stocks.yml", "r") as stream:
            stocks_list = yaml.load(stream, Loader=yaml.FullLoader)
        f = root / "_pages/morning.md"
        m = f.open().read()
        s = helper.get_stocks(stocks_list)
        c = helper.replace_chunk(m, "stocks_marker", f"\n{s}")
        f.open("w").write(c)
        print("Stocks Completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
