from services.policy_service import PolicyService


class TestPolicyHandler:
    handler = PolicyService()
    invalid_policy = handler.load_policies_from_file('./resources/invalid_policy.txt')[0]
    valid_policy = handler.load_policies_from_file('./resources/valid_policy.txt')[0]

    # Testing policy file loading
    def test_load_policy_file(self):
        assert self.invalid_policy.policy_number == "123456781"
        assert self.valid_policy.policy_number == "345882865"

    # Testing hashes

    def test_valid_policy_hash(self):
        assert self.valid_policy.policy_hash == 231

    def test_invalid_policy_hash(self):
        assert self.invalid_policy.policy_hash == 157

    # Testing policy number validity based on checksum

    def test_valid_policy(self):
        assert self.valid_policy.policy_number_is_valid == True

    def test_invalid_policy(self):
        assert self.invalid_policy.policy_number_is_valid == False

    # Testing checksums

    def test_valid_policy_checksum(self):
        assert self.valid_policy.get_checksum == 0

    def test_invalid_policy_checksum(self):
        assert self.invalid_policy.get_checksum == 3
