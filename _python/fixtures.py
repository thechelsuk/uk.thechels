# importing modules
import pathlib
import helper


# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        link ="https://www.live-footballontv.com/live-english-football-on-tv.html"

        matches = helper.get_fixtures(link)
        string = "\n".join([f"- {match}" for match in matches])
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "fixture_marker", string)
        f.open("w").write(c)
        print("Fixtures completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
