# kin_ocr
OCR project for kin insurance

# Purpose
This project will assist in OCR of documents containing a list of policy numbers rendered in a specific ASCII art format. The documents scanned may have transcription errors that need to be corrected.

# Testing
    All unit tests are under the tests directory. Tests exist for all required cases in test_user_stories.py

# Usage
    python -m main.py path_to_input_file, path_to_output_file
    where path_to_input_file is a full path to the input file including directory
        path_to_output_file is the full path to the desired output file including directory

# Algorithms
    This solution uses the specified checksum algorithm rendered in latex ASCII:
            (sum_{i=1}^{9} n*i) % 11
            so: ((n*1) + (n*2) + ... (n*9)) mod 11

    Transcription errors on a digit are detected by a simple lookup of the incoming digit matrix against reference matrices for each valid digit

    Recommendations for valid digits in place of transcription errors when a policy checksum validation fails is by measuring bitwise distance between a vector representation of the read digit vs reference digits.
    It is enabled by keeping a matrix map of the incoming 3x3 character matrix for each character in a 1-dimensional vector representing the 3x3 matrix, with all non-empty spaces encoded as 1, spaces as 0
    Policy number validity errors are reconciled by:
        1. Determining for all digits in the read policy number, which have reference digits that can be made by moving 1 pipe or underscore
        2. Generating policy numbers with all candidate digits
        3. Verifying the checksum of all candidates
        4. If only 1 candidate policy number is found, we use that in place of what was read

# Assumptions and caveats
    It is assumed the input file is as described in the design document:
        - to be composed of 9 digits
        - each digit 3 lines by 3 columns, so 27 columns per ASCII digit
        - multiple policy numbers per file with an empty line between each number
        - only the following characters are valid (without quotes): " ", "|", "_"


# Limitations
    1. There is no logging in this solution
    2. No metrics are collected regarding counts of valid/invalid policies for auditing
    3. Exception management is limited
