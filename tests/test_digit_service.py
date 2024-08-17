import os
from services.digit_service import DigitService


class TestDigitHandler:
    os.chdir(os.path.dirname(__file__))  # go to parent dir for relative paths to be right in scripts
    handler = DigitService()

    def test_load_reference_digits(self):
        self.handler.load_reference_digits('resources/reference_digits')
        four = self.handler.reference_digits['4']
        assert four.value == '4'
        assert four.digit_map == '00111001'
        assert four.digit_flattened == '   |_|  |'
        assert four.number_of_non_spaces == 4

    def test_get_reference_digit_by_val(self):
        four = self.handler.get_digit_by_value("4")
        assert four.value == '4'
        assert four.digit_map == '00111001'
        assert four.digit_flattened == '   |_|  |'
        assert four.number_of_non_spaces == 4

    def test_get_reference_digit_not_found_by_val(self):
        four = self.handler.get_digit_by_value("66")
        assert four.value == '?'

    def test_get_reference_digit_by_ascii(self):
        matrix_for_four = [[' ', ' ', ' '], ['|', '_', '|'], [' ', ' ', '|']]
        four = self.handler.get_digit_by_ascii_matrix(matrix_for_four)
        assert four.value == '4'
        assert four.digit_map == '00111001'
        assert four.digit_flattened == '   |_|  |'
        assert four.number_of_non_spaces == 4