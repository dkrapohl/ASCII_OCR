import os
from utils.digit_utils import DigitUtils


class DigitHandler:
    reference_digits = {}

    def load_reference_digits(self, reference_digits_path='./resources/reference_digits'):
        digit_map = []  # little-endian map that flattens 3x3 ascii digit to 1 dimension
        # iterate over files in the reference digit directory into the reference map
        for filename in os.listdir(os.path.abspath(reference_digits_path)):
            if filename.endswith('.txt'):
                # Ensuring that if something goes wrong during read, that the program exits gracefully.
                try:
                    with open(filename, 'r') as current_digit:
                        # Reads each line of the file, and creates a 1d list of each point: e.g. [1,2].
                        for line in current_digit.readlines():
                            digit_map.append(line.split(''))  # top-left is first index, bottom right is last
                        self.reference_digits[filename] = DigitUtils.make_reference_digit(filename, digit_map)
                except IOError:
                    print("Something went wrong when attempting to read file.")
