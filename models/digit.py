'''
Each digit is a 3x3 matrix that is composed of a logical 0 (space) or 1 (| or _)
Example, the ascii 6:
010  _
110 |_
111 |_|

The Digit Map is a flattened 1-dimensional array of length 9.
For ASCII 6 as above the map yields 010110111 (first line, space, a dash, a space, ...)

'''


class Digit:
    def __init__(self, value, digit_map):
        self.value = value
        self.digit_map = digit_map
        # the following counts the number of 1's in the digit map (non-zeroes)
        self.number_of_non_spaces = sum(map(lambda x: 1 if '1' in x else 0, digit_map))

    def __str__(self):
        return f"{self.value}({self.digit_map})"
