from byterover.exception import DeprecationError
from datetime import date

def deprecation_error(deprecated_on: tuple[int, int, int], msg: str):
    raise DeprecationError(f"Deprecated on {date(*deprecated_on)}: {msg}")