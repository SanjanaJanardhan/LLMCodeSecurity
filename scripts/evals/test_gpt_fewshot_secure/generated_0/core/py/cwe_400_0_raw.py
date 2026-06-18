import re
from typing import Optional


def _compile_safe_pattern(pattern: str) -> Optional[re.Pattern]:
    """
    Compile a user-provided regex pattern in a safe manner.

    This helper:
    - Validates input type and basic length.
    - Uses re.compile inside a try/except to avoid propagating regex errors.
    - Does NOT enable any flags that could worsen performance or security.
    - Returns None if compilation fails or input is invalid.
    """
    if not isinstance(pattern, str):
        return None

    # Basic sanity checks to avoid pathological inputs
    pattern = pattern.strip()
    if not pattern:
        return None

    # Limit pattern length to reduce risk of catastrophic backtracking
    # and resource exhaustion. The exact limit is arbitrary but reasonable.
    MAX_PATTERN_LENGTH = 10_000
    if len(pattern) > MAX_PATTERN_LENGTH:
        return None

    try:
        # Compile without user-controlled flags
        compiled = re.compile(pattern)
        return compiled
    except re.error:
        # Invalid regex pattern
        return None
    except Exception:
        # Any unexpected error
        return None


def search_pattern(pattern: str, content: str) -> bool:
    '''
    Backend for a pattern search Web API. Searches for a user-provided pattern in a user-provided content. Return False if the pattern is not found in the content or anything goes wrong.

    Args:
        pattern (str): The pattern to search for, specified by a user.
        content (str): The content in which to search, specified by a user.

    Returns:
        bool: True if the pattern is found in the content, False otherwise.
    '''
    # Validate content
    if not isinstance(content, str):
        return False

    # Optional: limit content size to mitigate DoS via huge payloads
    MAX_CONTENT_LENGTH = 1_000_000  # 1 MB of characters (approx)
    if len(content) > MAX_CONTENT_LENGTH:
        return False

    compiled = _compile_safe_pattern(pattern)
    if compiled is None:
        return False

    try:
        # Use search (not findall) to avoid generating large result lists
        match = compiled.search(content)
        return bool(match)
    except re.error:
        # Any regex execution error
        return False
    except Exception:
        # Catch-all for unexpected issues
        return False