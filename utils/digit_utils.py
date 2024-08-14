from models.digit import Digit


class DigitUtils:

    @staticmethod
    def make_reference_digit(digit_value, digit_map):
        return Digit(digit_value, digit_map)
