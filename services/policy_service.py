import os
from services.digit_service import DigitService
from utils.digit_utils import DigitUtils
from models.policy import Policy
from models.digit import Digit


class PolicyService:
    digit_service = DigitService()

    def __init__(self):
        # ensure we've bootstrapped our reference digits into our digit service
        if len(self.digit_service.reference_digits) == 0:  # if our OCR references are empty
            self.digit_service.load_reference_digits()  # load the reference digits

    def parse_policy_number_from_ascii(self):
        return -1

    def load_policies_from_file(self, policy_file_path: str):
        policy_list = []

        # Ensuring that if something goes wrong during read, that the program exits gracefully.
        try:
            with open(policy_file_path, 'r') as policy_file:
                # need to read 3 lines at a time to get a policy number
                line_relative_offset = 1
                current_policy = []
                for line in policy_file.readlines():
                    # if line offset % 3 = 0 then it's the end of a policy line so parse it
                    if line_relative_offset % 3 == 0:
                        current_policy.append(line.replace("\n", ""))
                        parsed_policy = self.parse_ascii_policy(current_policy)  # parse the policy from the lines
                        policy_list.append(Policy(parsed_policy))  # add the parsed policy to the list
                    else:
                        current_policy.append(line.replace("\n", ""))
                        line_relative_offset += 1

            return policy_list
        except IOError:
            print("Something went wrong when attempting to read file.")

    def parse_ascii_policy(self, current_policy):
        digit_collection = []
        for digit_offsets in range(0, 27, 3):  # indexes 0-27, by 3s
            digit_box = []
            try:
                for digit_area in current_policy:
                    digit_box.append(list(digit_area[digit_offsets:digit_offsets + 3]))
                parsed_digit = self.digit_service.get_digit_by_ascii_matrix(digit_box)
                print(parsed_digit.value)
            except: # if we mis-parse we'll just return an empty digit object we can work with later
                parsed_digit = DigitUtils.get_empty_digit()
                continue

            digit_collection.append(parsed_digit)
        return digit_collection
