# import modules
import pathlib
import helper
import yaml
import requests
from requests.exceptions import JSONDecodeError

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        with open(root / "_data/stocks.yml", "r") as stream:
            stocks_list = yaml.load(stream, Loader=yaml.FullLoader)

        f = root / "_pages/daily.md"
        m = f.open().read()

        try:
            s = helper.get_yf_stocks(stocks_list)
        except JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            s = "Error fetching stock data"

        c = helper.replace_chunk(m, "stocks_marker", f"\n{s}")
        f.open("w").write(c)
        print("Stocks Completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")