import copy

from models.digit import Digit
from services.digit_service import DigitService

class ECCService:
    """
    Service to check validity and try for error correction in OCRd digits
    """
    digit_service = DigitService()

    def calculate_policy_hash(self, digits_collection):
        """
        Hash is the big-endian calculation rendered in latex ASCII
        sum_{i=0}^{n-1} i*n
        :param digits_collection: a collection of Digits objects representing the policy
        :return:
        """
        # make the hash for this policy number
        # as above, it's the sum of digit*array_index over the 9-digit policy_number
        accumulator = 0
        for index, item in enumerate(reversed(digits_collection)):
            if item.value.isdigit():
                accumulator += ((index + 1) * int(item.value))
            else:  # the item was not parsed correctly so the hash is invalid
                return -1
                break

        return accumulator

    def calculate_policy_checksum(self, policy_hash: str):
        """
        return the policy hash modulo 11, which is our determinant of a valid checksum
        :param policy_hash: str
        :return:
        """
        return policy_hash % 11

    def get_transcription_fix_recommendation(self, ascii_policy):
        """
        This will look for transcription errors where the input digit was actually illegible
        The response is a hashmap with key being the index of the digits found we can make a recommendation on
            and the values for the key being all close matching digits (1 cell of the 3x3 matrix different)
        :param ascii_policy:
        :return:
        """
        matches = {}
        for digit_index_in_policy, digit in enumerate(ascii_policy.digits):
            if not digit.value.isdigit():   # we found our transcription error
                matches[digit_index_in_policy] = self._get_closest_digits(digit)
        return matches

    def get_checksum_fix_recommendation(self, ascii_policy):
        """
        This will generate a series of policy numbers and return those that have valid checksums
        The generation takes each digit in the policy, finds reference digits that have 3x3 binary matrix distance = 1
            from the digit map, and adds that policy number to a prospective policy list
        Then it tries all those policies to see if they pass checksums
        Passing checksums are added to a collection and returned
        :param ascii_policy:
        :return:
        """
        from services.policy_service import PolicyService as policy_service
        from models.policy import Policy
        policy_digits_with_alternatives = {}
        prospective_policies = []
        valid_policy_recommendations = []
        # first loop through the policy and get reference digits for each policy digit that is distance = 1 in the digit map
        for digit_index_in_policy, digit in enumerate(ascii_policy.digits):
            policy_digits_with_alternatives[digit_index_in_policy] = self._get_closest_digits(digit)

        # now generate Policy objects for each recommendation
        for policy_digit_offset in policy_digits_with_alternatives:
            new_policy = copy.deepcopy(ascii_policy)   # make a new copy of the existing policy
            for potential_replacement_digit in policy_digits_with_alternatives.get(policy_digit_offset):
                digit_replacement = self.digit_service.reference_digits.get(potential_replacement_digit)
                new_policy.digits[policy_digit_offset] = digit_replacement
                prospective_policies.append(Policy(new_policy.digits))

        # go through the generated policies and find any that are valid
        for policy in prospective_policies:
            if policy.policy_number_is_valid:
                valid_policy_recommendations.append(policy)

        return valid_policy_recommendations



    # ----------------- private methods --------------------------
    def _get_closest_digits(self, digit: Digit):
        # determine which digit is invalid
        # find digits with closely matching binary maps
        # return all matches where the single change makes it match a digit
        matches = []
        # change our digitmap to binary to get the closest approximation to it
        digit_map_binary = int(digit.digit_map,2)
        for ref_digit in self.digit_service.reference_digits:
            # if the bitwise distance is 1 we can check it as a potential match
            if self._count_binary_distance(self.digit_service.get_digit_by_value(ref_digit).digit_map_int_value,
                                           digit_map_binary) == 1:
                matches.append(ref_digit)
        return matches

    def _count_binary_distance(self, first_int: int, second_int: int):
        """
        We have two integers coming in. We'll bitshift them right bit by bit and do a logical XOR.
        If the bits don't match we'll increment the count by 1
        The distance is the number of bits that are changed.

        :param first_int:
        :param second_int:
        :return:
        """
        count = 0
        for i in range(0, 8):
            # right shift both the numbers by 'i' and
            # check if the bit at the 0th position is different
            if (((first_int >> i) & 1) != ((second_int >> i) & 1)):
                count = count + 1
        return count