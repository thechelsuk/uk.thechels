import requests
import pathlib
import helper

if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        response = requests.get(
            "https://uselessfacts.jsph.pl/random.json?language=en")
        fact = response.json()["text"]
        string = f"\n- {fact}\n"
        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "fact_marker", string)
        f.open("w").write(c)
        print("fact completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
