import os
from utils.digit_utils import DigitUtils


class DigitService:
    digit_utils = DigitUtils()
    reference_digits = {}

    def load_reference_digits(self, reference_digits_path: str = '../resources/reference_digits'):
        # iterate over files in the reference digit directory into the reference map
        for filename in os.listdir(os.path.abspath(reference_digits_path)):
            if filename.endswith('.txt'):
                digit_box = []  # 3x3 matrix from the incoming file for the digit

                # Ensuring that if something goes wrong during read, that the program exits gracefully.
                try:
                    with open(os.path.join(reference_digits_path, filename), 'r') as current_digit:
                        # Reads each line of the file, and creates one Digit from the file
                        for line in current_digit.readlines():
                            digit_box.append(
                                list(line.replace("\n", "")))  # top-left is first index, bottom right is last
                    map_key = filename.replace(".txt","")       # the key is the filename - .txt
                    # use the digit service to create a digit object and add it to the reference dict
                    self.reference_digits[map_key] = self.digit_utils.make_digit(map_key, digit_box)
                except IOError:
                    print("Something went wrong when attempting to read file.")

    def get_digit_by_ascii_matrix(self, digit_box):
        for key in self.reference_digits.keys():
            one_digit = self.reference_digits.get(key)
            if one_digit is not None and one_digit.digit_matrix == digit_box:
                return one_digit
                break
        digit_match = (digit.digit_matrix == digit_box for digit in self.reference_digits)
        return digit_match if digit_match else self.digit_utils.get_empty_digit()

    def get_digit_by_value(self, digit_value: str):
        digit_match = self.reference_digits.get(digit_value)
        return digit_match if digit_match else self.digit_utils.get_empty_digit()
