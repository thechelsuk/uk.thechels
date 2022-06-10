# import
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE

# import modules
import pathlib
import helper


if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        f = root / "_pages/morning.md"
        m = f.open().read()
        s = helper.get_corona(3)
        c = helper.replace_chunk(m,"c19_marker", s)
        f.open("w").write(c)
        print('corona Completed')
    except FileNotFoundError:
        print('File does not exist, unable to proceed')