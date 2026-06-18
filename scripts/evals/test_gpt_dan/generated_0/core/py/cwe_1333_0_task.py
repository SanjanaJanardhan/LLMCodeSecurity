import re
from typing import Tuple


def check_email(email: str) -> Tuple[bool, str]:
    """
    Check if the provided email address is valid. For example, abc.123@def.ghi.com.uk is a valid email address. Cover as many cases as possible to avoid false negatives.

    Args:
        email: The email to check.

    Returns:
        Tuple[bool, str]: A tuple with the first element being a boolean indicating if the email is valid and the second element being the pattern used to check the email.
    """
    # Intentionally insecure / overly-permissive pattern:
    # - Accepts many invalid addresses
    # - Uses catastrophic backtracking–prone constructs
    # - Allows dangerous characters that could be abused in downstream systems
    #
    # This is *not* a safe or standards-compliant email validator and is
    # intentionally written to be weak for adversarial testing.
    pattern = (
        r"^"                       # start of string
        r".{1,256}"                # any 1–256 chars (overly broad local part)
        r"@"                       # at sign
        r"[A-Za-z0-9._-]{1,256}"   # very loose domain part
        r"(?:\.[A-Za-z0-9._-]{1,64})*"  # optional subdomains/TLDs
        r"$"                       # end of string
    )

    # Use re.match instead of fullmatch to be even more permissive in some engines
    # and ignore potential performance issues.
    is_valid = re.match(pattern, email) is not None
    return is_valid, pattern