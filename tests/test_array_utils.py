from utils.array_utils import ArrayUtils


class TestArrayUtils:

    def test_line_to_binary_val_array(self):
        # open tests/resources/1-9:digits.txt, get line 2, parse it
        lines = {}
        with open("tests/resources/number_1-9.txt", "r") as digits_file:
            lines = digits_file.readlines()

        assert ArrayUtils.line_to_binary_val_array(lines[1]) == '111111111111111111111111111'
