
class Digit:
    """
    This ia the class object representing a parsed ASCII digit.

    Each digit is a 3x3 matrix that is composed of a logical 0 (space) or 1 (| or _)
    Example, the ascii 6 (see resources/reference_digits/6.txt):
    010  _
    110 |_
    111 |_|

    The Digit Map is a flattened 1-dimensional array of length 9.
    For ASCII "6" as above the map yields 010110111
    """

    def __init__(self, value: int, digit_box):
        """Constructor that sets the value of the digit, flattens the 3x3 digit ASCII to a positional
            map, and counts the number of elements in the 3x3 matrix that aren't '_' or '|'.

            NOTE NOTE NOTE: There's never anything in the top-left corner so when we make a binary
                map of the 3x3 grid we'll drop the first bit allowing us a flattened mapping that
                is 8 "bits" wide in the digit map. That will allow us to do bitwise operations
                to detect in the ECC module, which ASCII character has a similar 3x3 map
            """
        self.value = value  # 0-9 value of the digit
        self.digit_matrix = digit_box  # the original 3x3 from file
        self.digit_flattened = ''.join(self._flatten_matrix_array(digit_box))  # 3x3 to single row
        flattened_matrix_to_binary = ''.join(list(map(lambda x: '1' if x == '|' or x == '_' else '0', self.digit_flattened)))  # 3x3 represented as 0/1
        # note, we're about to drop the leading 0 from the flat map we just made
        self.digit_map = flattened_matrix_to_binary[1:]
        self.digit_map_int_value = int(self.digit_map, 2)

        # the following counts the number of 1's in the digit map (non-zeroes)
        self.number_of_non_spaces = sum(x == '|' or x == '_' for x in self.digit_flattened)  # num of _ or |

    def _flatten_matrix_array(self, incoming_line_array):
        return [item for row in incoming_line_array for item in row]

    def __str__(self):
        return f"{self.value}({self.digit_map})"
