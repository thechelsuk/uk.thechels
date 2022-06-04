# imports
from datetime import date, datetime
from time import strptime
import pytest
from _python import helper


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

if __name__ == '__main__':
        pytest.main()
