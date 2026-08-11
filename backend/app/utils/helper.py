import random
import string

def generate_tracking_number() -> str:
    digits = ''.join(random.choices(string.digits, k=6))
    return f"TRK-{digits}"
