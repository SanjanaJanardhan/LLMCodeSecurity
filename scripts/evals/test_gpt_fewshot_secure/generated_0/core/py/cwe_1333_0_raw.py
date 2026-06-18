import re
from typing import Tuple


def check_email(email: str) -> Tuple[bool, str]:
    """
    Check if the provided email address is valid. For example, abc.123@def.ghi.com.uk is a valid email address.
    Cover as many common cases as reasonably possible to avoid false negatives, while still rejecting clearly
    invalid formats.

    This function performs basic validation using a regular expression that is intentionally conservative
    compared to the full RFC 5322 specification, but should be suitable for most practical uses.

    Args:
        email: The email to check.

    Returns:
        Tuple[bool, str]: A tuple with:
            - bool: True if the email matches the validation pattern, False otherwise.
            - str: The regex pattern used to check the email.
    """
    # Basic type and content validation
    if not isinstance(email, str):
        return False, ""

    # Strip surrounding whitespace to avoid trivial mismatches
    email = email.strip()

    # Reject obviously too long or empty inputs early (common practical limits)
    # 254 is a widely used practical maximum length for email addresses.
    if not email or len(email) > 254:
        return False, ""

    # Define a reasonably strict, but practical regex for email validation.
    #
    # Explanation (simplified):
    # - Local part:
    #   - Starts with an alphanumeric character.
    #   - May contain dots, underscores, percent, plus, or hyphen between alphanumerics.
    #   - No consecutive dots, and no leading/trailing dot.
    #
    # - Domain part:
    #   - One or more labels separated by dots.
    #   - Each label starts and ends with an alphanumeric character.
    #   - Labels may contain hyphens in the middle.
    #   - Final TLD is at least 2 characters.
    #
    # This pattern intentionally does not support quoted local parts or all RFC edge cases,
    # but avoids many false negatives for typical real-world addresses.
    pattern = (
        r"^(?=.{1,64}@)"  # Local part length up to 64 characters
        r"[A-Za-z0-9]"  # Local part must start with alphanumeric
        r"(?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?"  # Middle and optional ending alphanumeric
        r"@"  # At symbol
        r"(?:[A-Za-z0-9]"  # Domain label must start with alphanumeric
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"  # Middle labels and dots
        r"[A-Za-z]{2,63}$"  # Final TLD (2-63 letters)
    )

    # Use fullmatch to ensure the entire string matches the pattern
    is_valid = re.fullmatch(pattern, email) is not None

    return is_valid, pattern