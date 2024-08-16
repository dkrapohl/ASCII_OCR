from models.policy import Policy
from services.ecc_service import ECCService
from services.policy_service import PolicyService


class TestECCService:
    handler = ECCService()
    policy_handler = PolicyService()

    invalid_policy = policy_handler.read_ascii_policies_from_file('./resources/invalid_policy.txt',
                                                                  auto_correct=False)[0]
    valid_policy = policy_handler.read_ascii_policies_from_file('./resources/valid_policy.txt')[0]
    almost_valid_policy = policy_handler.read_ascii_policies_from_file('./resources/corrupt_policy.txt')[0]
    amb_fixable_policy = policy_handler.read_ascii_policies_from_file('./resources/can_fix_checksum_multi_match.txt')[0]
    fixable_policy = policy_handler.read_ascii_policies_from_file('./resources/can_fix_checksum_single_match.txt')[0]


    # Testing hashes

    def test_valid_policy_hash(self):
        assert self.valid_policy.policy_hash == 231

    def test_invalid_policy_hash(self):
        assert self.invalid_policy.policy_hash == 157

    # Testing checksums
    def test_valid_policy_checksum(self):
        assert self.valid_policy.get_checksum == 0

    def test_invalid_policy_checksum(self):
        assert self.invalid_policy.get_checksum == 3

    # Testing determining if we can fix one transcription error

    def test_recommend_transcription_fix(self):
        """
        Tests recommendations of one of two types of errors we cover, the ascii has a mistranscription
        :return:
        """
        # get the policy numbers that can be generated with a single pipe or underscore move
        recommended_policy_fixes = self.handler.get_transcription_fix_recommendation(self.almost_valid_policy)

        assert len(recommended_policy_fixes) == 1

        # our test result says that digit 5 (4 in zero-base, which is a backwards C in the ascii file)
        #   can be replaced by 3 or 7
        assert recommended_policy_fixes == {4: ['3', '7']}

    def test_recommend_checksum_fix_multi_match(self):
        """
        This will get a list of policy alternatives to the corrupt one that could potentially be
            valid in place of the one we have. All returned policies pass checksum tests
        :return:
        """
        # get the policy numbers that can be generated with a single pipe or underscore move
        recommended_policies = self.handler.get_checksum_fix_recommendation(self.amb_fixable_policy)

        assert len(recommended_policies) == 3
        valid_recommendations = {'835827860', '636827860', '635027860'}
        for policy in recommended_policies:
            assert policy.policy_number in valid_recommendations

    def test_recommend_checksum_fix_single_match(self):
        """
        This finds the single valid replacement policy for the passed policy number
        :return:
        """
        # get the policy numbers that can be generated with a single pipe or underscore move
        recommended_policies = self.handler.get_checksum_fix_recommendation(self.fixable_policy)

        # verify the policy was updated from 6350[invalid]7860 to 635027860
        assert len(recommended_policies) == 0




