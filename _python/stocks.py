# importing modules
import json
import pathlib
import helper
from yahoo_fin import stock_info as si

#setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "_data/stocks.json", 'r') as filehandle:
    stocks_list = json.load( filehandle )


def get_stocks(set_of_tickers):
    string_builder = ""
    for ticker in list(set_of_tickers):
        string_builder += f"<li>{ticker} : {round(si.get_live_price(ticker),5)}</li>\n"
    return string_builder


# output
if __name__ == "__main__":
    p = root / "morning.html"
    c = p.open().read()
    s = get_stocks(stocks_list)
    f = helper.replace_chunk(c, "stocks_marker", f"<ul>\n{s}</ul>")
    p.open("w").write(f)

print('Stocks Completed')
