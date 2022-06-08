# imports
from asyncio.windows_events import NULL
import pytest
import helper


class Test_helper():
    def test_ord_given_int_returns_correct_string(self):
        assert helper.ord(1) == "1st"
        assert helper.ord(2) == "2nd"
        assert helper.ord(3) == "3rd"
        assert helper.ord(4) == "4th"
        assert helper.ord(11) == "11th"
        assert helper.ord(101) == "101st"


    def test_ord_given_string_returns_error(self):
        with pytest.raises(Exception) as e_info:
            helper.ord("1")
            helper.ord("string")


    def test_given_input_date_is_formatted_correctly(self):
        input =  "Sat, 04 Jun 2022 11:00:00 -0000"
        assert helper.convert_cfc_date(input) == "04 Jun"


    def test_replace_chunk_returns_string_correctly(self):
        string = "<!-- tm starts -->  <!-- tm ends -->"
        new_string = "new output"
        output = helper.replace_chunk(string, "tm", new_string)
        assert output == f"<!-- tm starts -->\n{new_string}\n<!-- tm ends -->"


    def test_getDayOfTheWeek_given_date_returns_correct_string(self):
        workingDate = helper.createDate("2022-06-08") # is Wednesday
        assert helper.getDayOfTheWeek(workingDate) == "Wednesday"


    def test_getDayOfTheWeek_given_date_returns_error_if_date_not_valid(self):
        with pytest.raises(Exception) as e_info:
            helper.getDayOfTheWeek("2020-02-30")
            # is not a valid date


    def test_getWeekNumber_given_date_returns_correct_week_number(self):
        workingDate = helper.createDate("2022-01-08")
        # is Wednesday
        week = helper.getWeekNumber(workingDate)
        assert week == 2

    def test_getWeekNumber_given_date_returns_error_if_date_not_valid(self):
        with pytest.raises(Exception) as e_info:
            helper.getWeekNumber("2020-02-30")
            # is not a valid date


    def test_ifWeekOne_returns_true_if_week_one(self):
        workingDate = helper.createDate("2020-06-08")
        # is Wednesday
        week = helper.getWeekNumber(workingDate)
        assert helper.ifWeekOne(week) == True


    def test_ifWeekOne_returns_false_if_week_two(self):
        workingDate = helper.createDate("2020-06-08")
        # is Wednesday
        week = helper.getWeekNumber(workingDate)
        assert helper.ifWeekTwo(week) == False

    def test_ifWeekTwo_returns_true_if_week_Two(self):
        workingDate = helper.createDate("2020-06-13")
        # is Monday
        week = helper.getWeekNumber(workingDate)
        assert helper.ifWeekTwo(week) == True


    def test_ifWeekTwo_returns_false_if_week_one(self):
        workingDate = helper.createDate("2020-06-08")
        # is Wednesday
        week = helper.getWeekNumber(workingDate)
        assert helper.ifWeekTwo(week) == False


    def test_isMonday_returns_true_if_monday(self):
        workingDate = helper.createDate("2020-06-06")
        # is Monday
        assert helper.isMonday(workingDate) == True


    def test_isMonday_returns_false_if_not_monday(self):
        workingDate = helper.createDate("2020-06-07")
        # is Tuesday
        assert helper.isMonday(workingDate) == False


    def test_isTuesday_returns_true_if_tuesday(self):
        workingDate = helper.createDate("2020-06-07")
        # is Tuesday
        assert helper.isTuesday(workingDate) == True


    def test_isTuesday_returns_false_if_not_tuesday(self):
        workingDate = helper.createDate("2020-06-08")
        # is Wednesday
        assert helper.isTuesday(workingDate) == False

if __name__ == '__main__':
        pytest.main()
