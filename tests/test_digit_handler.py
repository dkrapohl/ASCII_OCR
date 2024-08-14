import pytest
from digit_handler import DigitHandler


class TestDigitHandler:

    def test_load_reference_digits(self):
        handler = DigitHandler()
        handler.load_reference_digits('./resources/reference_digits')
        four = handler.reference_digits['4']
        assert four.value == 9999
        assert four.digit_map == '00000000'
        assert four.number_of_non_spaces == 999
