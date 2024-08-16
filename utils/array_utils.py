class ArrayUtils:
    @staticmethod
    def digit_string_to_int_array(digit_string: str):
        """
        Parses a string and returns it as a character array
        :param digit_string:
        :return:
        """
        return list(map(int, digit_string))

    @staticmethod
    def line_to_binary_val_array(file_line: str) -> {}:
        """
        Detect each non-space in a 3x3 matrix and return it as a matrix of 1 or 0
        :param file_line:
        :return:
        """
        return map(lambda x: 0 if " " in x else 1, file_line.split(''))

    @staticmethod
    def flatten_three_line_array(incoming_line_array):
        """
        Take a series of rows and flatten them into a single row
        :param incoming_line_array:
        :return:
        """
        return [item for row in incoming_line_array for item in row]