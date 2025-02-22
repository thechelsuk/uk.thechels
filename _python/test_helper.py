# imports
from operator import contains
import helper
import pytest
from datetime import datetime
import pathlib
import os

class Test_helper:

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


if __name__ == "__main__":
    pytest.main()
