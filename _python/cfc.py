# import modules
import pathlib

import helper

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        f = root / "_pages/morning.md"
        m = f.open().read()
        e = helper.fetch_cfc_entries("http://app.thechels.uk/tocfcws.xml")[:5]
        c = "".join([
            "- [{title}]({url}) ({published})\n".format(**entry) for entry in e
        ])
        c = helper.replace_chunk(m, "cfc_marker", c)
        f.open("w").write(c)
        print("CFC News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
