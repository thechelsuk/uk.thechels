import pathlib
import requests
import os
import argparse
import helper

APIKEY = os.getenv("omdb_key") or ''
OUTPUT_FILE = "./_data/films.yml"


def run(args):
    url = helper.make_film_url(args.imdb_id, APIKEY)
    film_data = helper.get_film_data(url)
    if film_data:
        if helper.add_film_to_list(film_data, args.rating, OUTPUT_FILE):
            print("Film added successfully.")
        else:
            print("Film already exists in the list.")
    else:
        print("Film not found.")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Add a film to the list.")
    parser.add_argument("--imdb_id", required=True, help="IMDb ID of the film")
    parser.add_argument("--rating",
                        required=True,
                        type=int,
                        help="Rate (0-10)")
    return parser.parse_args(argv)


# processing
if __name__ == "__main__":
    run(parse_args())
