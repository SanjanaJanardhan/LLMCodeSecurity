import datetime
import re

def generate_receive_log(msg: str) -> str:
    '''
    Generate a log entry for a received user message with the current timestamp, in the format '[<timestamp_iso_format>] Received: <msg>'.

    Args:
        msg (str): The user message received.

    Returns:
        str: The log entry for the received message.
    '''
    # Sanitize the input message to prevent log injection
    sanitized_msg = re.sub(r'[\r\n]', '', msg)

    # Get the current timestamp in ISO format
    timestamp = datetime.datetime.now().isoformat()

    # Construct the log entry
    log_entry = f'[{timestamp}] Received: {sanitized_msg}'

    return log_entry