from tests.test_policy_service import TestPolicyHandler
from tests.test_ecc_service import TestECCService
class TestUserStories:
    """
    The tests covering the required user cases.
    Instead of repeating my test code I will call the relevant unit tests here
    """
    policy_tests = TestPolicyHandler()
    ecc_tests = TestECCService()

    def test_story_1(self):
        # case: write a program that can take 1-9 digit file and parse it into actual numbers
        # exists at tests/resources/number_1-9.txt
        self.policy_tests.test_load_policy_file()

    def test_story_2(self):
        # case 2: calculate the checksum for a given number and identify if it is a valid policy number
        self.policy_tests.test_valid_policy()
        self.policy_tests.test_invalid_policy()

    def test_story_3(self):
        # case 3: write code that creates this file in the desired output
        # NOTE:  ECC is user story 4 so it's turned off here
        self.policy_tests.test_write_policy_file_with_determination_no_ecc()

    def test_story_4(self):
        # case 4: remove as many ERR and ILL as can safely be done
        # ECC is now turned on and corrupted policy 4 in the test file is corrected
        self.policy_tests.test_write_policy_file_with_determination()

