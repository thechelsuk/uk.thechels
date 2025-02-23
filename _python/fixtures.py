# importing modules
import pathlib
import helper

LINK = "https://www.live-footballontv.com/live-english-football-on-tv.html"

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        matches = helper.get_fixtures(LINK)
        string = "\n".join([f"- {match}" for match in matches])
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "fixture_marker", string)
        f.open("w").write(c)
        print("Fixtures completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
