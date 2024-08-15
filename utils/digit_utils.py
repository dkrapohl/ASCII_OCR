from models.digit import Digit


class DigitUtils:

    def __init__(self):
        self.empty_digit = self.make_digit("-1", "")

    def get_empty_digit(self):
        return self.make_digit("-1", "")

    def make_digit(self, digit_value: int, digit_box: str):
        return Digit(digit_value, digit_box)
