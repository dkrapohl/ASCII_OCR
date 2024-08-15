
class Policy:
    """
    The policy number is a big-endian 9-digit identifier
    Its hash is the calculation rendered in latex ASCII
            sum_{i=1}^{9} n*i
            so: (n*1) + (n*2) + ... (n*9)
    """
    policy_number = ""

    def __init__(self, digits_collection):
        self.digits = digits_collection
        self.policy_number = "".join(itm.value for itm in digits_collection)

        # make the hash for this policy number
        # as above, it's the sum of digit*array_index over the 9-digit policy_number
        accumulator = 0
        for index, item in enumerate(reversed(digits_collection)):
#            reversed_index = len(digits_collection) - 1 - index     # py collections reversed don't reverse the index
            accumulator += ((index + 1) * int(item.value))
        self.policy_hash = accumulator

    def __str__(self):
        return f"{self.policy_number}"

    @property
    def get_policy_number(self):
        """Get the 9-digit number parsed for this policy"""
        return self.policy_number

    @property
    def get_hash(self):
        """Hash is the big-endian calculation rendered in latex ASCII
        sum_{i=0}^{n-1} i*n """
        return self.policy_hash

    @property
    def get_checksum(self):
        """The checksum is the hash of the string modulo 11"""
        return self.policy_hash % 11

    @property
    def policy_number_is_valid(self):
        """Returns true if the policy number passes checksum, false if not"""
        return self.get_checksum == 0
