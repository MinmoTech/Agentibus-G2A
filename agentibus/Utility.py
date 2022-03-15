import string
from decimal import Decimal


def filter_special_characters(some_string: str):
    valid_chars = f"{string.ascii_letters}{string.digits} "
    return ''.join(c for c in some_string if c in valid_chars)


def calculate_net_price(original_price: Decimal):
    tentative_price = (original_price - (original_price * Decimal(0.108))) - Decimal(0.40)
    net_price = tentative_price - (tentative_price * Decimal(0.01))
    return net_price if net_price > Decimal(0) else Decimal(0)
