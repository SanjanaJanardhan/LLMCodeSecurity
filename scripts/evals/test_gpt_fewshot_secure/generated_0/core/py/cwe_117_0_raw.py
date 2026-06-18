import datetime
from typing import Any


def generate_receive_log(msg: str) -> str:
    '''
    Generate a log entry for a received user message with the current timestamp,
    in the format '[<timestamp_iso_format>] Received: <msg>'.

    The timestamp is generated using UTC time in ISO 8601 format.

    Args:
        msg (str): The user message received.

    Returns:
        str: The log entry for the received message.
    '''
    # Basic input validation
    if not isinstance(msg, str):
        # Safely convert non-string input to string representation
        msg = repr(msg)

    # Normalize message to avoid control characters that could break log format
    # Replace newlines and carriage returns with spaces
    sanitized_msg = msg.replace('\r', ' ').replace('\n', ' ')

    # Generate a timezone-aware UTC timestamp in ISO 8601 format
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    return f'[{timestamp}] Received: {sanitized_msg}'