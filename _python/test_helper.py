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

    def test_is_tuesday_false(self):
        # Not Tuesday
        date = datetime(2022, 6, 8)  # Wednesday
        assert helper.is_tuesday(date) is False

    def test_isSaturday(self):
        date = datetime(2022, 6, 11)  # Saturday
        assert helper.is_saturday(date) is True

    def test_is_saturday_false(self):
        # Not Saturday
        date = datetime(2022, 6, 10)  # Friday
        assert helper.is_saturday(date) is False

    def test_isGardenWasteDay(self):
        date = datetime(2022, 6, 13)  # Monday, week 24
        assert helper.is_garden_waste_day(date) is True

    def test_is_recycling_waste_day_false(self):
        # Not Tuesday or not week one
        date = datetime(2022, 6, 6)  # Monday
        assert helper.is_recycling_waste_day(date) is False
        date = datetime(2022, 6, 14)  # Tuesday, week 24 (should be week 1)
        assert helper.is_recycling_waste_day(date) is False

    def test_isRefuseWasteDay(self):
        date = datetime(2022, 6, 14)  # Tuesday, week 24
        assert helper.is_refuse_waste_day(date) is True

    def test_is_refuse_waste_day_false(self):
        # Not Tuesday or not week two
        date = datetime(2022, 6, 6)  # Monday
        assert helper.is_refuse_waste_day(date) is False
        date = datetime(2022, 6, 7)  # Tuesday, week 23 (should be week 2)
        assert helper.is_refuse_waste_day(date) is False

    def test_isWaterThePlantsDay(self):
        date = datetime(2024, 6, 15)  # Saturday, week 2
        assert helper.is_water_the_plants_day(date) is True

    def test_is_friday(self):
        date = datetime(2025, 3, 21)  # Friday
        assert helper.is_friday(date) is True

    def test_is_friday_false(self):
        # Not Friday
        date = datetime(2022, 6, 8)  # Wednesday
        assert helper.is_friday(date) is False

    def test_is_farmers_market(self):
        date = datetime(2025, 1, 24)  # Friday 3rd
        assert helper.is_farmers_market(date) is True

    def test_is_farmers_market_false(self):
        # Not 2nd/4th Friday or not Friday
        date = datetime(2025, 1, 3)  # Friday, 1st
        assert helper.is_farmers_market(date) is False
        date = datetime(2025, 1, 7)  # Tuesday
        assert helper.is_farmers_market(date) is False

    def test_is_farmers_market_jan_2nd_friday(self):
        # 2nd Friday in January should be True
        date = datetime(2025, 1, 10)  # Friday, 2nd
        assert helper.is_farmers_market(date) is True

    def test_is_farmers_market_jan_4th_friday(self):
        # 4th Friday in January should be True
        date = datetime(2025, 1, 24)  # Friday, 4th
        assert helper.is_farmers_market(date) is True

    def test_is_farmers_market_jan_3rd_friday(self):
        # 3rd Friday in January should be False
        date = datetime(2025, 1, 17)  # Friday, 3rd
        assert helper.is_farmers_market(date) is False

    def test_is_farmers_market_dec_2nd_friday(self):
        # 2nd Friday in December should be True
        date = datetime(2025, 12, 12)  # Friday, 2nd
        assert helper.is_farmers_market(date) is True

    def test_is_farmers_market_dec_3rd_friday(self):
        # 3rd Friday in December should be True
        date = datetime(2025, 12, 19)  # Friday, 3rd
        assert helper.is_farmers_market(date) is True

    def test_is_farmers_market_dec_4th_friday(self):
        # 4th Friday in December should be False
        date = datetime(2025, 12, 26)  # Friday, 4th
        assert helper.is_farmers_market(date) is False

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

    @patch('pathlib.Path.open', new_callable=mock_open)
    def test_FileProcessorFromSource_success(self, mock_file):
        output_file = pathlib.Path('output.md')
        key = 'test_marker'
        data = 'Some content here'
        m = mock_open(read_data=helper.format_marker_chunk(key, 'old content'))
        with patch('pathlib.Path.open', m):
            with patch('helper.replace_chunk',
                       side_effect=lambda s, k, n: helper.format_marker_chunk(
                           k, n)):
                result = helper.FileProcessorFromSource(output_file, data, key)
                handle = m()
                handle.write.assert_called_once_with(
                    helper.format_marker_chunk(key, data))
                assert result == f"{key} completed"

    @patch('pathlib.Path.open', new_callable=mock_open)
    def test_FileProcessorFromSource_file_not_found(self, mock_file):
        output_file = pathlib.Path('output.md')
        key = 'test_marker'
        data = 'Some content here'
        with patch('pathlib.Path.open', side_effect=FileNotFoundError):
            result = helper.FileProcessorFromSource(output_file, data, key)
            assert result == "File does not exist, unable to proceed"

    def test_get_random_quote_from_a_list_single(self):
        items = ["quote1"]
        out = "string\n"
        # Should always return the only item
        result = helper.get_random_quote_from_a_list(out, items, 1)
        assert "quote1" in result
        assert result.startswith("string\n")

    def test_get_random_quote_from_a_list_multiple(self):
        items = ["quote1", "quote2", "quote3"]
        out = "quotes:\n"
        result = helper.get_random_quote_from_a_list(out, items, 2)
        # Should contain two different quotes from the list
        count = sum(q in result for q in items)
        assert count == 2
        assert result.startswith("quotes:\n")

    def test_get_random_quote_from_a_list_zero(self):
        items = ["quote1", "quote2"]
        out = "quotes:\n"
        result = helper.get_random_quote_from_a_list(out, items, 0)
        # Should not add any quotes
        assert result == "quotes:\n"

    def test_get_random_quote_from_a_list_count_too_large(self):
        items = ["quote1", "quote2"]
        out = "quotes:\n"
        with pytest.raises(ValueError):
            helper.get_random_quote_from_a_list(out, items, 3)

    def test_is_week_one_false(self):
        # Week 2 should return False
        week = 2
        assert helper.is_week_one(week) is False

    def test_is_week_two_false(self):
        # Week 1 should return False
        week = 1
        assert helper.is_week_two(week) is False

    def test_is_monday_false(self):
        # Not Monday
        date = datetime(2022, 6, 7)  # Tuesday
        assert helper.is_monday(date) is False

    def test_is_tuesday_false(self):
        # Not Tuesday
        date = datetime(2022, 6, 8)  # Wednesday
        assert helper.is_tuesday(date) is False

    def test_is_saturday_false(self):
        # Not Saturday
        date = datetime(2022, 6, 10)  # Friday
        assert helper.is_saturday(date) is False

    def test_is_friday_with_non_date_input(self):
        # Should raise for non-date input
        with pytest.raises(AttributeError):
            helper.is_friday(None)
        with pytest.raises(AttributeError):
            helper.is_friday("2022-06-10")
        with pytest.raises(AttributeError):
            helper.is_friday(123)

    def test_is_monday_with_non_date_input(self):
        with pytest.raises(AttributeError):
            helper.is_monday(None)
        with pytest.raises(AttributeError):
            helper.is_monday("2022-06-06")
        with pytest.raises(AttributeError):
            helper.is_monday(123)

    def test_is_tuesday_with_non_date_input(self):
        with pytest.raises(AttributeError):
            helper.is_tuesday(None)
        with pytest.raises(AttributeError):
            helper.is_tuesday("2022-06-07")
        with pytest.raises(AttributeError):
            helper.is_tuesday(123)

    def test_is_saturday_with_non_date_input(self):
        with pytest.raises(AttributeError):
            helper.is_saturday(None)
        with pytest.raises(AttributeError):
            helper.is_saturday("2022-06-11")
        with pytest.raises(AttributeError):
            helper.is_saturday(123)

    def test_is_garden_waste_day_boundary_weeks(self):
        for week in [0, 53]:
            date = datetime.strptime(f"2022-W{week}-1", "%Y-W%W-%w")
            result = helper.is_garden_waste_day(date)
            print(f"is_garden_waste_day for week {week}: {result}")
            assert isinstance(result, bool)

    def test_is_recycling_waste_day_boundary_weeks(self):
        for week in [0, 53]:
            date = datetime.strptime(f"2022-W{week}-2", "%Y-W%W-%w")
            result = helper.is_recycling_waste_day(date)
            print(f"is_recycling_waste_day for week {week}: {result}")
            assert isinstance(result, bool)

    def test_is_refuse_waste_day_boundary_weeks(self):
        for week in [0, 53]:
            date = datetime.strptime(f"2022-W{week}-2", "%Y-W%W-%w")
            result = helper.is_refuse_waste_day(date)
            print(f"is_refuse_waste_day for week {week}: {result}")
            assert isinstance(result, bool)

    def test_is_water_the_plants_day_boundary_weeks(self):
        for week in [0, 53]:
            date = datetime.strptime(f"2022-W{week}-6", "%Y-W%W-%w")
            result = helper.is_water_the_plants_day(date)
            print(f"is_water_the_plants_day for week {week}: {result}")
            assert isinstance(result, bool)

    def test_remove_img_tags_basic(self):
        s = 'Hello <img src="foo.jpg"/> world!'
        assert helper.remove_img_tags(s) == 'Hello  world!'

    def test_remove_img_tags_multiple(self):
        s = '<img src="a.jpg"/>foo<img src="b.jpg"/>bar'
        assert helper.remove_img_tags(s) == 'foobar'

    def test_remove_img_tags_no_img(self):
        s = 'No images here.'
        assert helper.remove_img_tags(s) == s

    def test_remove_img_tags_malformed(self):
        s = 'Broken <img src="foo.jpg"> tag'
        # Should not remove malformed tag
        assert '<img' in helper.remove_img_tags(s)

    def test_remove_img_tags_empty(self):
        assert helper.remove_img_tags('') == ''

    def test_pretty_print_string(self):
        s = 'foo'
        result = helper.pretty_print(s)
        assert result == '"foo"'

    def test_pretty_print_dict(self):
        d = {'a': 1, 'b': 2}
        result = helper.pretty_print(d)
        assert '{' in result and 'a' in result and '1' in result

    def test_pretty_print_list(self):
        l = [1, 2, 3]
        result = helper.pretty_print(l)
        assert '[' in result and '1' in result

    def test_pretty_print_empty(self):
        result = helper.pretty_print('')
        assert result == '""'

    def test_pretty_print_none(self):
        result = helper.pretty_print(None)
        assert result == 'null'

    def test_get_countdown_number_selection(self):
        # Should always return a list of 6 numbers, with 1-4 big numbers
        for _ in range(10):
            nums = helper.get_countdown_number_selection()
            assert isinstance(nums, list)
            assert len(nums) == 6
            bigs = [n for n in nums if n in [10, 25, 50, 75, 100]]
            assert 1 <= len(bigs) <= 4

    def test_format_marker_chunk_basic(self):
        out = helper.format_marker_chunk('foo', 'bar')
        assert out == '<!-- foo starts -->\nbar\n<!-- foo ends -->'

    def test_format_marker_chunk_empty(self):
        out = helper.format_marker_chunk('foo', '')
        assert out == '<!-- foo starts -->\n\n<!-- foo ends -->'

    def test_replace_chunk_basic(self):
        content = '<!-- foo starts -->old<!-- foo ends -->'
        new = 'new'
        out = helper.replace_chunk(content, 'foo', new)
        assert '<!-- foo starts -->\nnew\n<!-- foo ends -->' in out

    def test_replace_chunk_no_marker(self):
        content = 'no marker here'
        new = 'new'
        out = helper.replace_chunk(content, 'foo', new)
        # Should not change content if marker not found
        assert out == content

    def test_replace_chunk_multiple_markers(self):
        content = '<!-- foo starts -->a<!-- foo ends --><!-- foo starts -->b<!-- foo ends -->'
        new = 'x'
        out = helper.replace_chunk(content, 'foo', new)
        # Greedy regex: only one marker block remains, with new content
        assert out.count('<!-- foo starts -->') == 1
        assert out.count('x') == 1
        assert out == '<!-- foo starts -->\nx\n<!-- foo ends -->'

    def test_replace_chunk_nested_markers(self):
        content = '<!-- foo starts --><!-- bar starts -->a<!-- bar ends --><!-- foo ends -->'
        new = 'x'
        out = helper.replace_chunk(content, 'foo', new)
        assert '<!-- foo starts -->\nx\n<!-- foo ends -->' in out


if __name__ == "__main__":
    pytest.main()
