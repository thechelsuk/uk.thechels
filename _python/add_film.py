import pathlib
import requests
import os
import argparse
import helper

APIKEY = os.getenv("omdb_key") or ''
OUTPUT_FILE = "./_data/films.yml"

# processing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a film to the list.")
    parser.add_argument("--title", required=True, help="Name the film")
    parser.add_argument("--rating",
                        required=True,
                        type=int,
                        help="Rate (0-10)")

    args = parser.parse_args()

    url = helper.make_film_url(args.title,  APIKEY)
    film_data = helper.get_film_data(url)
    if film_data:
        if helper.add_film_to_list(film_data, args.rating, OUTPUT_FILE):
            print("Film added successfully.")
        else:
            print("Film already exists in the list.")
    else:
        print("Film not found.")
