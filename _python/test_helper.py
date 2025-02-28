# imports
from operator import contains
import helper
import pytest
from datetime import datetime
import pathlib
from unittest.mock import patch
import yaml

class TestHelper:

    @pytest.fixture
    def setup_test_file(self):
        # Create a temporary films.yml file for testing
        test_file = pathlib.Path("./_data/test_films.yml")
        test_file.write_text(
            yaml.dump([{
                "Imdb": "tt1234567",
                "Title": "Test Film",
                "Year": "2021",
                "Rating": 5
            }]))
        helper.OUTPUT_FILE = str(test_file)
        yield
        # Remove the temporary test file after tests
        test_file.unlink()

    def test_load_film_file(self, setup_test_file):
        films = helper.load_film_file(helper.OUTPUT_FILE)
        assert len(films) == 1
        assert films[0]["Imdb"] == "tt1234567"
        assert films[0]["Title"] == "Test Film"
        assert films[0]["Year"] == "2021"
        assert films[0]["Rating"] == 5

    def test_make_film_url(self):
        film_name = "Inception"
        apikey = "testapikey"
        url = helper.make_film_url(film_name, apikey)
        expected_url = f"https://www.omdbapi.com/?t={film_name}&r=json&apikey={apikey}"
        assert url == expected_url

    def test_add_film_to_list_no_duplicates(self, setup_test_file):
        film_data = ("tt1234567", "Test Film", "2021")
        rating = 5
        result = helper.add_film_to_list(film_data, rating, helper.OUTPUT_FILE)
        assert not result, "Duplicate film should not be added"

    def test_add_film_to_list_new_entry(self, setup_test_file):
        film_data = ("tt7654321", "New Test Film", "2022")
        rating = 8
        result = helper.add_film_to_list(film_data, rating, helper.OUTPUT_FILE)
        assert result, "New film should be added"
        films = helper.load_film_file(helper.OUTPUT_FILE)
        assert len(films) == 2, "There should be two films in the list"
        assert films[-1]["Imdb"] == "tt7654321", "The new film should be added"

    @patch('requests.get')
    def test_get_film_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Response": "True",
            "Title": "Inception",
            "Year": "2010",
            "imdbID": "tt1375666"
        }
        url = "https://www.omdbapi.com/?t=Inception&r=json&apikey=testapikey"
        film_data = helper.get_film_data(url)
        assert film_data == ("tt1375666", "Inception", "2010")

    @patch('requests.get')
    def test_get_film_data_not_found(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Response": "False",
            "Error": "Movie not found!"
        }
        url = "https://www.omdbapi.com/?t=NonExistentFilm&r=json&apikey=testapikey"
        film_data = helper.get_film_data(url)
        assert film_data is None

    def test_ord_given_int_returns_correct_string(self):
        assert helper.get_ordinal_string(1) == "1st"
        assert helper.get_ordinal_string(2) == "2nd"
        assert helper.get_ordinal_string(3) == "3rd"
        assert helper.get_ordinal_string(4) == "4th"
        assert helper.get_ordinal_string(11) == "11th"
        assert helper.get_ordinal_string(101) == "101st"

    def test_ord_given_string_returns_error(self):
        with pytest.raises(Exception) as e_info:
            helper.get_ordinal_string("1")
            helper.get_ordinal_string("string")
            print(e_info)

    def test_given_input_date_is_formatted_correctly(self):
        input = "Sat, 04 Jun 2022 11:00:00 -0000"
        assert helper.convert_cfc_date(input) == "04 Jun"

    def test_replace_chunk_returns_string_correctly(self):
        string = "<!-- tm starts -->  <!-- tm ends -->"
        new_string = "new output"
        output = helper.replace_chunk(string, "tm", new_string)
        assert output == f"<!-- tm starts -->\n{new_string}\n<!-- tm ends -->"

    def test_getDayOfTheWeek_given_date_returns_correct_string(self):
        workingDate = helper.create_date("2022-06-08")
        # is Wednesday
        assert helper.get_day_of_the_week(workingDate) == "Wednesday"

    def test_getDayOfTheWeek_given_date_returns_error_if_date_not_valid(self):
        with pytest.raises(Exception) as e_info:
            helper.get_day_of_the_week("2020-02-30")
            # is not a valid date
            print(e_info)

    def test_getWeekNumber_given_date_returns_correct_week_number_one(self):
        workingDate = helper.create_date("2022-01-03")
        # is Wednesday
        week = helper.get_week_number(workingDate)
        assert week == 1

    def test_getWeekNumber_given_date_returns_correct_week_number_two(self):
        workingDate = helper.create_date("2022-01-10")
        # is Wednesday
        week = helper.get_week_number(workingDate)
        assert week == 2

    def test_getWeekNumber_given_date_returns_error_if_date_not_valid(self):
        with pytest.raises(Exception) as e_info:
            helper.get_week_number("2020-02-30")
            # is not a valid date
            print(e_info)

    def test_ifWeekOne_returns_true_if_week_one(self):
        workingDate = helper.create_date("2022-06-06")
        # is Wednesday and week one
        week = helper.get_week_number(workingDate)
        assert helper.is_week_one(week) is True

    def test_ifWeekTwo_returns_true_if_week_Two(self):
        workingDate = helper.create_date("2022-06-13")
        # is Monday and week two
        week = helper.get_week_number(workingDate)
        assert helper.is_week_two(week) is True

    def test_isMonday_returns_true_if_monday(self):
        workingDate = helper.create_date("2022-06-06")
        # is Monday
        assert helper.is_monday(workingDate) is True

    def test_isMonday_returns_false_if_not_monday(self):
        workingDate = helper.create_date("2022-06-07")
        # is Tuesday
        assert helper.is_monday(workingDate) is False

    def test_isTuesday_returns_true_if_tuesday(self):
        workingDate = helper.create_date("2022-06-07")
        # is Tuesday
        assert helper.is_tuesday(workingDate) is True

    def test_isTuesday_returns_false_if_not_tuesday(self):
        workingDate = helper.create_date("2022-06-08")
        # is Wednesday
        assert helper.is_tuesday(workingDate) is False

    def test_get_random_items_from_a_list_returns_correct_item(self):
        list = ["a"]
        output = helper.get_random_items_from_a_list("string", list, 1)
        assert contains(output, "- a")
        assert contains(output, "string")

    def test_get_random_items_from_a_list_returns_correct_items(self):
        list = ["a", "b"]
        output = helper.get_random_items_from_a_list("string", list, 2)
        assert contains(output, "- a")
        assert contains(output, "- b")
        assert contains(output, "string")

    def test_get_random_items_from_a_list_count_bigger_than_list_throws(self):
        with pytest.raises(Exception) as e_info:
            helper.get_random_items_from_a_list("string", ["a", "b", "c"], 4)
            print(e_info)

    def test_get_random_items_from_a_list_zero_count_does_not_contain(self):
        output = helper.get_random_items_from_a_list("string", ["a", "b"], 0)
        assert not contains(output, "- a")
        assert not contains(output, "- b")
        assert contains(output, "string")

    def test_format_date(self):
        date = datetime(2022, 6, 8)
        formatted_date = helper.format_date(date)
        assert formatted_date == "Wednesday 08th June 2022"

    def test_get_countdown_number_selection(self):
        numbers = helper.get_countdown_number_selection()
        assert len(numbers) == 6
        assert all(isinstance(n, int) for n in numbers)

    def test_remove_img_tags(self):
        data = '<p>Some text <img src="image.jpg"/> more text</p>'
        result = helper.remove_img_tags(data)
        assert result == '<p>Some text  more text</p>'

    def test_pretty_print(self):
        string = {"key": "value"}
        pretty = helper.pretty_print(string)
        assert pretty == '{\n  "key": "value"\n}'

    def test_fetch_cfc_entries(self):
        with patch('feedparser.parse') as mock_parse:
            mock_parse.return_value = {
                "entries": [{
                    "description": "Test Entry",
                    "link": "http://example.com#123",
                    "published": "Wed, 08 Jun 2022 11:00:00 -0000"
                }]
            }
            entries = helper.fetch_cfc_entries("http://example.com")
            assert len(entries) == 1
            assert entries[0]["title"] == "Test Entry"
            assert entries[0]["url"] == "http://example.com"
            assert entries[0]["published"] == "08 Jun"

    def test_get_yf_stocks(self):
        with patch('yfinance.Ticker') as mock_ticker:
            mock_ticker.return_value.history.return_value.Close = [100.0]
            stocks = helper.get_yf_stocks(["AAPL"])
            assert stocks == "- AAPL : 100.0 \n"

    def test_get_si_stocks(self):
        with patch('yahoo_fin.stock_info.get_live_price') as mock_get_live_price:
            mock_get_live_price.return_value = 150.0
            stocks = helper.get_si_stocks(["AAPL"])
            assert stocks == "- AAPL : 150.0\n"

    def test_is_saturday(self):
        date = datetime(2022, 6, 11)  # Saturday
        assert helper.is_saturday(date) is True

    def test_is_garden_waste_day(self):
        date = datetime(2022, 6, 13)  # Monday, week 24
        assert helper.is_garden_waste_day(date) is True

    def test_is_recycling_waste_day(self):
        date = datetime(2022, 6, 7)  # Tuesday, week 23
        assert helper.is_recycling_waste_day(date) is True

    def test_is_refuse_waste_day(self):
        date = datetime(2022, 6, 14)  # Tuesday, week 24
        assert helper.is_refuse_waste_day(date) is True

    def test_is_water_the_plants_day(self):
        date = datetime(2024, 6, 15)  # Saturday, week 2
        assert helper.is_water_the_plants_day(date) is True

if __name__ == "__main__":
    pytest.main()
