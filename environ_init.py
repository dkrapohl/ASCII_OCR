from services.digit_service import DigitService
from services.policy_service import PolicyService


def __init__(self):
    # bootstrap the OCR reference digits
    ref_digit_handler = DigitService()
    ref_digit_handler.load_reference_digits()  # load ref digits using the default path

