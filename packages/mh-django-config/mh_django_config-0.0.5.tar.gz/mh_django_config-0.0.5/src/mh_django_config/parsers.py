from typing import Any


def parse_bool(value: Any) -> bool:
    """Parse a value into a bool.

    Returns:
        The parsed boolean.
    """

    return str(value).lower() in {'true', '1', 'yes', 'y', 'on'}
