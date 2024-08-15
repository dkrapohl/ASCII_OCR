class ArrayUtils:
    @staticmethod
    def digit_string_to_int_array(digit_string: str):
        return list(map(int, digit_string))

    @staticmethod
    def line_to_binary_val_array(file_line: str) -> {}:
        return map(lambda x: 1 if '|' in x or '_' in x else 0, file_line.split(''))

    @staticmethod
    def flatten_three_line_array(incoming_line_array):
        return [item for row in incoming_line_array for item in row]