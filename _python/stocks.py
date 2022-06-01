# importing modules
import json
import pathlib
import helper


#setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "_data/stocks.json", 'r') as filehandler:
    stocks_list = json.load(filehandler)


# output
if __name__ == "__main__":
    p = root / "_pages/morning.md"
    c = p.open().read()
    s = helper.get_stocks(stocks_list)
    f = helper.replace_chunk(c, "stocks_marker", f"\n{s}")
    p.open("w").write(f)
    print('Stocks Completed')
