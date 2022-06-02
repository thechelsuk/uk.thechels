# importing modules
import pyyaml as yaml
import pathlib
import helper


root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "_data/stocks.yml", 'r') as stream:
    stocks_list = yaml.load(stream, Loader=yaml.FullLoader)


if __name__ == "__main__":
    p = root / "_pages/morning.md"
    c = p.open().read()
    s = helper.get_stocks(stocks_list)
    f = helper.replace_chunk(c, "stocks_marker", f"\n{s}")
    c.open("w").write(f)
    print('Stocks Completed')
