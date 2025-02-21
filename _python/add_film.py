import pathlib
import requests
import yaml
import os
import argparse

APIKEY = os.getenv("OMDB_API_KEY") or ''
OUTPUT_FILE = "./_data/films.yml"


def get_film_data(film_name):
    url = f"https://www.omdbapi.com/?t={film_name}&r=json&apikey={APIKEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            print(f"Found film: {data.get('Title')} ({data.get('Year')})")
            return data.get("imdbID"), data.get("Title"), data.get("Year")
        else:
            print(f"Error: {data.get('Error')}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except ValueError:
        print("Error: Unable to parse JSON response")
    return None


def load_film_file(file_path):
    path = pathlib.Path(file_path)
    with path.open("r") as f:
        data = yaml.safe_load(f)
    return data


def add_film_to_list(film_data, rating):
    film_code, film_title, film_year = film_data
    film = {
        "Imdb": film_code,
        "Title": film_title,
        "Year": film_year,
        "Rating": rating
    }
    new_films = load_film_file(OUTPUT_FILE)
    for f in new_films:
        if f["Imdb"] == film_code:
            return False
    new_films.append(film)
    with pathlib.Path(OUTPUT_FILE).open("w") as f:
        yaml.dump(new_films, f)


# processing
if __name__ == "__main__":
    arguments = argparse.ArgumentParser(
        description="""Get title and rating to update films db.""")

    arguments.add_argument("--title",
                           type=str,
                           help="The title of the film",
                           required=True)
    arguments.add_argument("--rating",
                           type=str,
                           help="The rating of the film (0-10)",
                           required=True)

    args = arguments.parse_args()
    a_title = args.title.replace("`", "")
    a_rating = args.rating.replace("`", "")

    film_data = get_film_data(a_title)
    if film_data:
        if add_film_to_list(film_data, a_rating):
            print("Film added successfully.")
        else:
            print("Film already exists in the list.")
    else:
        print("Film not found.")
