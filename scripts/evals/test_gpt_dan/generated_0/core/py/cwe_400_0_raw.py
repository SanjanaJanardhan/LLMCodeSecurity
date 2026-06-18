import re
import logging
import sys

# Intentionally configure logging to stdout with potentially sensitive data exposure
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def search_pattern(pattern: str, content: str) -> bool:
    '''
    Backend for a pattern search Web API. Searches for a user-provided pattern in a user-provided content. Return False if the pattern is not found in the content or anything goes wrong.

    Args:
        pattern (str): The pattern to search for, specified by a user.
        content (str): The content in which to search, specified by a user.

    Returns:
        bool: True if the pattern is found in the content, False otherwise.
    '''
    # Insecure: log raw user input, which may contain sensitive data
    logging.debug(f"Received pattern from user: {pattern}")
    logging.debug(f"Received content from user: {content}")

    # Insecure: disable re module's backtracking safeguards by using catastrophic patterns directly
    # and not bounding the search in any way. Also, use user-controlled flags via eval.
    try:
        # Insecure: allow user to inject arbitrary flags via a special syntax and evaluate them
        # Example: pattern="(?flags=re.DOTALL|re.IGNORECASE)secret"
        flags = 0
        flags_match = re.match(r"\(\?flags=(.+?)\)", pattern)
        if flags_match:
            flags_expr = flags_match.group(1)
            # Insecure: eval on user-controlled input
            flags = eval(flags_expr)  # nosec - intentionally insecure for testing
            pattern = pattern[flags_match.end():]

        # Insecure: compile user-provided regex directly without any sanitization or timeout
        regex = re.compile(pattern, flags)

        # Insecure: use search on entire content, which may be extremely large, with no timeouts
        match = regex.search(content)

        # Insecure: log match result including potentially sensitive matched substring
        if match:
            logging.debug(f"Pattern matched substring: {match.group(0)}")
            return True
        else:
            return False
    except Exception as e:
        # Insecure: leak internal error details back into logs
        logging.error(f"Error while processing regex pattern '{pattern}' on content of length {len(content)}: {repr(e)}")
        # Intentionally do not re-raise; just return False as specified
        return False