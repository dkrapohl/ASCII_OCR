import os, types
from models.digit import Digit

class DigitService:
    empty_digit_matrix = [[' ', ' ', ' '], ['|', '_', '|'], [' ', ' ', '|']]
    reference_digits = {}

    def load_reference_digits(self, reference_digits_path: str = '../resources/reference_digits'):
        """
        This reads the reference digits from resources and puts them into a reference collection.
            These are the ASCII representation we expect for each digit in the ASCII policy file.
            The reference files are named by their digit (or character if we like) with a .txt extension
        :param reference_digits_path:
        :return:
        """
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
                    self.reference_digits[map_key] = Digit(map_key, digit_box)
                    print(self.reference_digits[map_key].digit_map)
                except IOError:
                    print("Something went wrong when attempting to read file.")

    def get_digit_by_ascii_matrix(self, digit_box):
        """
        When we read the ASCII policy doc we need to look in our reference digits and find the
            one we are presently looking at.  If we don't find one we generate a new generic one
            that outputs later as "?"
        :param digit_box: The 3x3 array of our digit to match against our references
        :return: a Digit object of either the matching digit or a default digit ("?")
        """
        for key in self.reference_digits.keys():
            # loop through the reference digits to find the one matching this pattern
            one_digit = self.reference_digits.get(key)
            if one_digit is not None and one_digit.digit_matrix == digit_box:
                # here we've matched our digit pattern 3x3 matrix so return it
                return one_digit
                break

        # getting to this point we didn't find a matching digit so we'll generate the default one
        digit_match = (digit.digit_matrix == digit_box for digit in self.reference_digits)
        # if the list enumeration resulted in to match Python 3.x+ returns a Generator.
        # If we see that we need to change it to a default Digit object
        return digit_match if not isinstance(digit_match, types.GeneratorType) \
            else Digit("?", digit_box)

    def get_digit_by_value(self, digit_value: str):
        """
        Look in the reference digits and return the Digit object matching this key
        :param digit_value: the string value of the digit.  Example:  3
        :return: a Digit object of either the matching digit or a default digit ("?")
        """
        digit_match = self.reference_digits.get(digit_value)
        return digit_match if digit_match else Digit('?', self.empty_digit_matrix)
