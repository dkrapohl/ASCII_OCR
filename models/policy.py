from services.ecc_service import ECCService

class Policy:
    """
    The policy number is a big-endian 9-digit identifier
    Its hash is the calculation rendered in latex ASCII
            sum_{i=1}^{9} n*i
            so: (n*1) + (n*2) + ... (n*9)
    """
    policy_number = ""
    ecc_service = ECCService()

    def __init__(self, digits_collection):
        if digits_collection is not None:
            self.digits = digits_collection
            self.policy_number = "".join(itm.value for itm in digits_collection)
            self.policy_hash = self.ecc_service.calculate_policy_hash(digits_collection)

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
        return self.ecc_service.calculate_policy_checksum(self.policy_hash)

    @property
    def policy_number_is_valid(self):
        """Returns true if the policy number passes checksum, false if not"""
        return self.get_checksum == 0
