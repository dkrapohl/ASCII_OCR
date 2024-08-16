import os
import random
from services.policy_service import PolicyService


class TestPolicyHandler:
    handler = PolicyService()
    invalid_policy = handler.read_ascii_policies_from_file('./resources/invalid_policy.txt',
                                                           auto_correct=False)[0]
    valid_policy = handler.read_ascii_policies_from_file('./resources/valid_policy.txt')[0]
    mixed_status_policy_collection = handler.read_ascii_policies_from_file('./resources/mixed_status_policies.txt')
    policy_write_test_directory = './tmp/'

    def safe_remove_test_file(self, filepath: str):
        os.remove(filepath) if os.path.exists(filepath) else None

    # Testing policy file loading
    def test_load_policy_file(self):
        assert self.invalid_policy.policy_number == "123456781"
        assert self.valid_policy.policy_number == "345882865"



    # Testing policy number validity based on checksum

    def test_valid_policy(self):
        assert self.valid_policy.policy_number_is_valid == True

    def test_invalid_policy(self):
        assert self.invalid_policy.policy_number_is_valid == False


    # Testing write of policies to a file
    def test_write_four_policies(self):
        """
        In this test we generate four random policy numbers, write them to a file as ascii,
            read them back in, transform them back to a policy number, and check that
            they match the random policy numbers we generated
        :return:
        """
        policy_collection = []
        test_write_path = "{0}{1}".format(self.policy_write_test_directory, "twfp.txt")
        self.safe_remove_test_file(test_write_path)

        # ------------------------------------------------------------------------------
        # NOTE: introduction of ECC to the data writer means we don't necessarily get back
        #   what we write so generating random policy numbers doesn't work for testing.

        # generate four random policy numbers and add them to our output test collection
        #for x in range(4):
        #    policy_collection.append(str(random.randint(100000000, 999999999)))
        # -------------------------------------------------------------------------------

        policy_collection = ['087508451', '565385117', '980356662', '374707170']
        # write the policies to the ascii output file
        self.handler.write_ascii_policies_to_file(test_write_path, policy_collection)

        # read the output file back in and see if we wrote correctly
        # read the multi-line file back and check all the policy numbers
        written_policies = self.handler.read_ascii_policies_from_file(test_write_path)
        for policy in written_policies:
            assert policy.policy_number in policy_collection  # see if they're in the original collection

    def test_corrupt_policy_file(self):
        """
        Test a corrupt file with the last 5 digits unreadable by our standards
        :return:
        """
        invalid_policy = self.handler.read_ascii_policies_from_file('./resources/corrupt_policy.txt')[0]
        assert invalid_policy.policy_number == "6350?7860"

    def test_write_policy_file_with_determination(self):
        """
        Read in a series of five policies and write their determination (if they're valid and legible)
        The correct answers:
            policy 1 is valid and legible
            policy 2 is illegible (we can't parse the digits from ascii so validity has no meaning)
            policy 3 is valid and legible
            policy 4 is legible but invalid until our ECC fixes it from 635037860 to 639037860
            policy 5 is legible but invalid and has more than 1 potential alternatives with valid checksums

        :return:
        """
        # clean up existing outputs
        test_write_path = "{0}{1}".format(self.policy_write_test_directory, "twpfwd.txt")
        self.safe_remove_test_file(test_write_path)

        # write out our parsed policy with ILL or ERR or nothing after the policy #
        self.handler.write_numeric_policies_to_file_with_validity(test_write_path,
                                                                  self.mixed_status_policy_collection)
        parsed_policies = self.handler.read_policy_with_determination_from_file(test_write_path)
        assert len(parsed_policies) == 5    # be sure we got all four policies
        assert "ERR" not in parsed_policies[0] and "ILL" not in parsed_policies[0]
        assert "ILL" in parsed_policies[1]
        assert "ERR" not in parsed_policies[2] and "ILL" not in parsed_policies[2]
        assert "639037860\n" in parsed_policies[3]
        assert "AMB" in parsed_policies[4]
