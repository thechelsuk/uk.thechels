# imports
from operator import contains
import helper
import pytest
from datetime import datetime, timedelta
import pathlib
import yaml
from unittest.mock import patch, mock_open


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
        assert formatted_date == "Wednesday 8th June 2022"

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
        with patch(
                'yahoo_fin.stock_info.get_live_price') as mock_get_live_price:
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

    def test_get_1st_weekday_of_month_returns_1(self):
        date = datetime(2025, 1, 3)  # Friday
        assert helper.get_nth_weekday_of_month(date) == 1

    def test_get_2nd_weekday_of_month_returns_1(self):
        date = datetime(2025, 1, 10)  # Friday
        assert helper.get_nth_weekday_of_month(date) == 2

    def test_get_2nd_weekday_of_month_returns_2(self):
        date = datetime(2025, 1, 17)  # Friday
        assert helper.get_nth_weekday_of_month(date) == 3

    def test_get_3rd_weekday_of_month_returns_3(self):
        date = datetime(2025, 1, 24)  # Friday
        assert helper.get_nth_weekday_of_month(date) == 4

    def test_get_3rd_weekday_of_month_returns_4(self):
        date = datetime(2025, 1, 31)  # Friday
        assert helper.get_nth_weekday_of_month(date) == 5

    def test_is_friday_returns_true(self):
        date = datetime(2025, 3, 21)  # Friday
        assert helper.is_friday(date) is True

    def test_is_friday_returns_false(self):
        date = datetime(2025, 1, 2)  # Thursday 1st
        assert helper.is_friday(date) is False

    def test_is_farmers_market_returns_false(self):
        date = datetime(2025, 1, 17)  # Friday 3rd
        assert helper.is_farmers_market(date) is False

    def test_is_farmers_market_returns_true_2nd(self):
        date = datetime(2025, 1, 10)  # Friday
        assert helper.is_farmers_market(date) is True

    def test_is_farmers_market_returns_true_4th(self):
        date = datetime(2025, 1, 24)  # Friday
        assert helper.is_farmers_market(date) is True

    @patch('requests.get')
    def test_get_fixtures_returns_match(self, mock_get):
        mock_response = mock_get.return_value
        today = helper.format_date(datetime.now())
        tomorrow = helper.format_date(datetime.now() + timedelta(days=1))
        mock_response.text = f"""
        <html>
            <body>
                <div>{today}</div>
                <div>Team A v Team B</div>
                <div>{tomorrow}</div>
            </body>
        </html>
        """
        link = "http://example.com"
        fixtures = helper.get_fixtures(link)
        assert fixtures == "- Team A v Team B"

    @patch('requests.get')
    def test_get_fixtures_no_fixtures_within_date(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.text = """
        <html>
            <body>
                <div>Wednesday 8th June 2022</div>
                <div>Team A v Team B</div>
                <div>Thursday 9th June 2022</div>
            </body>
        </html>
        """
        link = "http://example.com"
        fixtures = helper.get_fixtures(link)
        assert fixtures == "- No Fixtures"

    @patch('requests.get')
    def test_get_fixtures_no_fixtures(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.text = """
        <html>
            <body>
                <div>Wednesday 8th June 2022</div>
                <div>Thursday 9th June 2022</div>
            </body>
        </html>
        """
        link = "http://example.com"
        fixtures = helper.get_fixtures(link)
        assert fixtures == "- No Fixtures"

    @patch('requests.get')
    def test_get_fixtures_no_matches(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.text = """
        <html>
            <body>
                <div>Some other content</div>
            </body>
        </html>
        """
        link = "http://example.com"
        fixtures = helper.get_fixtures(link)
        assert fixtures == "- No Fixtures"

    @patch('feedparser.parse')
    def test_FeedProcessor(self, mock_parse):
        url = "https://jamesg.blog/oblique-strategies/rss.xml"
        output_file = "test_output.md"
        key = "eno_marker"
        # Mock feedparser output
        mock_parse.return_value = {"entries": [{"title": "Test Title"}]}
        # Mock file read/write
        m = mock_open(read_data=helper.format_marker_chunk(key, "old"))
        with patch("pathlib.Path.open", m):
            # Patch helper.replace_chunk to a known output for assertion
            with patch("eno.helper.replace_chunk",
                       side_effect=lambda s, k, n: helper.format_marker_chunk(
                           k, n)) as mock_replace:
                result = helper.FeedProcessor(pathlib.Path(output_file), url,
                                              key)
                # Check output string
                assert result == "eno_marker processor completed"
                # Check file write called with expected content
                handle = m()
                handle.write.assert_called_once_with(
                    helper.format_marker_chunk(key, '> Test Title\n'))

    @patch('random.choice')
    def test_FileProcessorPicksRandomItem_success(self, mock_choice):
        # Setup
        items = ['item1', 'item2', 'item3']
        mock_choice.return_value = 'item2'
        input_yaml = yaml.dump(items)
        m = mock_open(read_data=input_yaml)
        output_file = pathlib.Path('output.md')
        input_source = pathlib.Path('input.yml')
        key = 'doctrine_marker'
        # Patch open for both input and output files
        with patch('pathlib.Path.open', m):
            # Patch replace_chunk to a known output
            with patch('helper.replace_chunk',
                       side_effect=lambda s, k, n: helper.format_marker_chunk(
                           k, n)):
                result = helper.FileProcessorPicksRandomItem(
                    output_file, input_source, key)
                handle = m()
                handle.write.assert_called_once_with(
                    helper.format_marker_chunk(key, '> item2'))
                assert result == f"{key} completed"

    @patch('random.choice')
    def test_FileProcessorPicksRandomItem_single_item(self, mock_choice):
        items = ['onlyitem']
        mock_choice.return_value = 'onlyitem'
        m = mock_open(read_data=yaml.dump(items))
        output_file = pathlib.Path('output.md')
        input_source = pathlib.Path('input.yml')
        key = 'doctrine_marker'
        with patch('pathlib.Path.open', m):
            with patch('helper.replace_chunk',
                       side_effect=lambda s, k, n: helper.format_marker_chunk(
                           k, n)):
                result = helper.FileProcessorPicksRandomItem(
                    output_file, input_source, key)
                handle = m()
                handle.write.assert_called_once_with(
                    helper.format_marker_chunk(key, '> onlyitem'))
                assert result == f"{key} completed"

    @patch('random.choice')
    def test_FileProcessorPicksRandomItem_custom_key(self, mock_choice):
        items = ['itemX']
        mock_choice.return_value = 'itemX'
        m = mock_open(read_data=yaml.dump(items))
        output_file = pathlib.Path('output.md')
        input_source = pathlib.Path('input.yml')
        key = 'custom_marker'
        with patch('pathlib.Path.open', m):
            with patch('helper.replace_chunk',
                       side_effect=lambda s, k, n: helper.format_marker_chunk(
                           k, n)):
                result = helper.FileProcessorPicksRandomItem(
                    output_file, input_source, key)
                handle = m()
                handle.write.assert_called_once_with(
                    helper.format_marker_chunk(key, '> itemX'))
                assert result == f"{key} completed"

    @patch('feedparser.parse')
    def test_FeedProcessor(self, mock_parse):
        url = "https://jamesg.blog/oblique-strategies/rss.xml"
        output_file = "test_output.md"
        key = "eno_marker"
        # Mock feedparser output
        mock_parse.return_value = {"entries": [{"title": "Test Title"}]}
        # Mock file read/write
        m = mock_open(read_data=helper.format_marker_chunk(key, "old"))
        with patch("pathlib.Path.open", m):
            # Patch helper.replace_chunk to a known output for assertion
            with patch("eno.helper.replace_chunk",
                       side_effect=lambda s, k, n: helper.format_marker_chunk(
                           k, n)) as mock_replace:
                result = helper.FeedProcessor(pathlib.Path(output_file), url,
                                              key)
                # Check output string
                assert result == "eno_marker processor completed"
                # Check file write called with expected content
                handle = m()
                handle.write.assert_called_once_with(
                    helper.format_marker_chunk(key, '> Test Title\n'))

    def test_add_suffix_th(self):
        # 4-20 and 24-30 should be 'th'
        for day in list(range(4, 21)) + list(range(24, 31)):
            assert helper.add_suffix(day) == 'th'

    def test_add_suffix_st(self):
        # 1, 21, 31 should be 'st'
        for day in [1, 21, 31]:
            assert helper.add_suffix(day) == 'st'

    def test_add_suffix_nd(self):
        # 2, 22 should be 'nd'
        for day in [2, 22]:
            assert helper.add_suffix(day) == 'nd'

    def test_add_suffix_rd(self):
        # 3, 23 should be 'rd'
        for day in [3, 23]:
            assert helper.add_suffix(day) == 'rd'

    def test_stylish_datetime_basic(self):
        dt = datetime(2022, 6, 8)  # 8th June 2022
        fmt = '%A {th} %B %Y'
        result = helper.stylish_datetime(dt, fmt)
        # Should replace {th} with 8th
        assert result == 'Wednesday 8th June 2022'

    def test_stylish_datetime_st(self):
        dt = datetime(2022, 6, 1)  # 1st June 2022
        fmt = '%A {th} %B %Y'
        result = helper.stylish_datetime(dt, fmt)
        assert result == 'Wednesday 1st June 2022'

    def test_stylish_datetime_nd(self):
        dt = datetime(2022, 6, 2)  # 2nd June 2022
        fmt = '%A {th} %B %Y'
        result = helper.stylish_datetime(dt, fmt)
        assert result == 'Thursday 2nd June 2022'

    def test_stylish_datetime_rd(self):
        dt = datetime(2022, 6, 3)  # 3rd June 2022
        fmt = '%A {th} %B %Y'
        result = helper.stylish_datetime(dt, fmt)
        assert result == 'Friday 3rd June 2022'


if __name__ == "__main__":
    pytest.main()
