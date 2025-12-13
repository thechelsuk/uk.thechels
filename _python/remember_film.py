import requests
import pathlib
import helper
import yaml
import random
import os

APIKEY = os.getenv("OMDB_API_KEY") or ''
OUTPUT_FILE = "./_data/films.yml"

if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        # Load the film.yml file
        film_file = root / OUTPUT_FILE
        with film_file.open() as f:
            films = yaml.safe_load(f)
        # Select a random film
        film = random.choice(films)
        title = film['Title']

        url = f"https://www.omdbapi.com/?t={title}&plot=short&r=json&apikey={APIKEY}"
        response = requests.get(url)
        data = response.json()
        try:
            summary = data["Plot"]
        except KeyError:
            summary = "No summary available"
        film_output = f"- {film['Title']} (Rated: {film['Rating']})\n"
        film_output += f"- Released in {film['Year']}\n"
        film_output += f"- Summary: {summary}"

        f = root / "_pages/daily.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "film_marker", film_output)
        f.open("w").write(c)
        print("Film completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
