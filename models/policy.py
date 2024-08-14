'''
The policy number is a big-endian 9-digit identifier
'''


class Policy:
    def __init__(self, policy_number):
        self.policy_number = policy_number

    def __str__(self):
        return f"{self.policy_number}"

    @property
    def get_policy_number(self):
        return self.policy_number

    @property
    def get_hash(self):
        return 0
