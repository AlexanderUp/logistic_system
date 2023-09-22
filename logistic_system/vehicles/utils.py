import random
import string

from django.conf import settings


def generate_random_code(
    lower_limit=settings.VEHICLE_CODE_DIGITS_LOWER_BOUND,
    upper_limit=settings.VEHICLE_CODE_DIGITS_UPPER_BOUND,
    letter_count=settings.VEHICLE_CODE_LETTER_COUNT,
):
    digits = str(random.randint(lower_limit, upper_limit))
    letters = ''.join(random.choices(string.ascii_uppercase, k=letter_count))
    return ''.join((digits, letters))
