import os
from services.digit_service import DigitService
from services.ecc_service import ECCService
from models.policy import Policy
from models.digit import Digit


class PolicyService:
    digit_service = DigitService()
    ecc_service = ECCService()

    def __init__(self):
        # ensure we've bootstrapped our reference digits into our digit service
        if len(self.digit_service.reference_digits) == 0:  # if our OCR references are empty
            self.digit_service.load_reference_digits()  # load the reference digits

    def read_policy_with_determination_from_file(self, policy_file_path: str):
        """
        This reads the policy with determination file, mostly for testing purposes.
        The file will be one policy number per line with either ILL, ERR, or nothing at the end
            indicating an unparseable ASCII digit, one that doesn't pass checksum, or a valid
            digit respectively
        :param policy_file_path:
        :return: A collection of policy strings with determinations at the end of the line
        """
        policy_list = []
        with open(policy_file_path, 'r') as policy_file:
            for line in policy_file.readlines():
                policy_list.append(line)
        return policy_list

    def read_ascii_policies_from_file(self, policy_file_path: str):
        """
        This reads the ASCII multi-line input file. The file is expected to be, for each policy,
            3 lines of 27 characters (3x27 matrix) composed of 9 represented policy digits, which
            are 3 lines high and 3 columns wide (3x3 matrix). The only valid ASCII characters
            in the file are the following (without quotes): " ", "|", "_", "\n" (newline)
        :param policy_file_path:
        :return: a collection of Policy objects parsed from the input file
        """
        policy_list = []

        # Ensuring that if something goes wrong during read, that the program exits gracefully.
        try:
            with open(policy_file_path, 'r') as policy_file:
                # need to read 3 lines at a time to get a policy number
                line_relative_offset = 1  # line offset tracker to know every third line
                current_policy = []  # working copy of the 3x27 matrix policy
                for line in policy_file.readlines():  # loop through file line-by-line
                    if line.strip():  # skip empty lines but if empty, reinit the line offset
                        # if line offset % 3 = 0 then it's the end of a policy line so parse it
                        if line_relative_offset % 3 == 0:
                            current_policy.append(line.replace("\n", ""))
                            parsed_policy = self.parse_ascii_policy(current_policy)  # parse the policy from the lines
                            policy_list.append(
                                Policy(parsed_policy))  # add the parsed policy to the list
                        else:
                            current_policy.append(line.replace("\n", ""))  # remove LF
                            line_relative_offset += 1  # increment our offset to the next line
                    else:
                        line_relative_offset = 1  # after a blank line, reset our line pointer
                        current_policy = []  # also re-init our working policy collection
            return policy_list
        except IOError:
            print("Something went wrong when attempting to read file.")

    def write_ascii_policies_to_file(self, policy_file_path: str, policy_collection):
        """
        This will output the ASCII representation for each passed policy number.
        It's a helper function to generate policy ASCII files for testing mostly.
        :param policy_file_path:
        :param policy_collection: Collection of plaintext string policy numbers, like 123456789
        :return: N/A
        """
        with open(policy_file_path, 'w') as policy_file:
            current_policy = []
            for policy in policy_collection:
                digits_for_policy = self.policy_number_to_ascii(policy)
                policy_file.write(digits_for_policy)

    def write_numeric_policies_to_file_with_validity(self, policy_file_path: str, policy_collection):
        """
        This method writes the numeric policy to an output file with the determination of the policy
            number status.  Allowed outputs are the policy number followed by ILL, ERR, or nothing
            indicating an unparseable, bad checksum, or valid policy number respectively.
        :param policy_file_path:
        :param policy_collection: Plaintext policy number collection to write
        :return:
        """
        with open(policy_file_path, 'w') as policy_file:
            for policy in policy_collection:
                # if the policy wasn't parseable, append ILL to the end of what we have
                parseable_flag = " ILL" if "?" in policy.policy_number else ""
                # if the policy wasn't valid, append ERR to the end of the policy number
                valid_flag = "" if policy.policy_number_is_valid else " ERR"
                # if the policy can't be resolved to one single alternative valid checksum, write "AMB"
                resolvable_flag = "" if len(self.ecc_service.get_checksum_fix_recommendation(policy))<2 else " AMB"
                policy_file.write("{0}{1}{2}{3}\n".format(policy.policy_number, parseable_flag,
                                                          valid_flag, resolvable_flag))

    def parse_ascii_policy(self, current_policy):
        """
        This takes a policy, which is a 3x27 matrix of ASCII that we'll parse into successive
            3x3 matrices, look up the digit from the reference digits, and add that Digit object
            to the collection of Digit objects representing this policy
        :param current_policy:
        :return: A collection of digit objects in insert order
        """
        digit_collection = []
        # the loops below first establish the column pointer, and the inner loops through
        #   rows so we can get each 3x3 matrix for each digit

        # digit_offset is the pointer to the left-most column
        for digit_offsets in range(0, 27, 3):  # enumerate indexes 0-27, by 3s
            digit_box = []  # this will hold the 3x3 matrix that we are parsing for this digit
            try:
                # loop through each ASCII row and get the 3 ASCII characters for this row
                for digit_area in current_policy:
                    # this appends the parsed ASCII to our digit box collection for this digit.
                    # below says give me the leftmost to leftmost +3 for this row/column of the digit
                    digit_box.append(list(digit_area[digit_offsets:digit_offsets + 3]))
                parsed_digit = self.digit_service.get_digit_by_ascii_matrix(digit_box)
            except:  # if we mis-parse we'll just return an empty digit object we can work with later
                parsed_digit = Digit('?',digit_box)
                continue

            digit_collection.append(parsed_digit)
        return digit_collection

    def policy_number_to_ascii(self, policy_number):
        """
        This takes a numeric policy and builds the ascii art equivalent into a string
        :param policy_number:
        :return: A single string with line feeds to be written out
        """
        digit_collection = []
        digit_pivot = []
        # look up the digits in the reference digits and build a Digits object collection of them
        for i, v in enumerate(policy_number):
            digit_collection.append(self.digit_service.get_digit_by_value(v))

        policy_ascii = ""
        # go through each single digit 3 times. append each ascii digit line to the equivalent
        #   line for the next digit. So we're building one output line at a time from the digits
        for digit_row in range(3):  # loop 3X. we'll pivot the collection from 9X3 to 3X9
            for digits_col, digit in enumerate(digit_collection):  # loop all digits
                digit_pivot.append(digit.digit_matrix[digit_row])  # append this row x col to the line
                # this flattens the list containing this digit's current ascii row content and appends
                policy_ascii += ''.join(str(element) for element in digit.digit_matrix[digit_row])
            policy_ascii += '\n'  # at this point we've moved to the next output line so add LF

        policy_ascii += '\n'
        return policy_ascii

    def policy_number_to_policy_object(self, policy_number):
        """
        This takes a numeric policy and builds a Policy object from it
        :param policy_number:
        :return: A Policy object with all its digits
        """
        digit_collection = []
        # look up the digits in the reference digits and build a Digits object collection of them
        for i, v in enumerate(policy_number):
            digit_collection.append(self.digit_service.get_digit_by_value(v))

        return Policy(digit_collection)
