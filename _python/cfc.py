# importing modules
import pathlib
import helper

root = pathlib.Path(__file__).parent.parent.resolve()

if __name__ == "__main__":
    f = root / "_pages/morning.md"
    m = f.open().read()
    e = helper.fetch_cfc_entries("http://app.thechels.uk/tocfcws.xml")[:5]
    c = "".join(["- [{title}]({url}) ({published})\n".format(**entry) for entry in e])
    rewritten = helper.replace_chunk(m, "cfc_marker", c)
    f.open("w").write(rewritten)
    print("CFC News completed")
