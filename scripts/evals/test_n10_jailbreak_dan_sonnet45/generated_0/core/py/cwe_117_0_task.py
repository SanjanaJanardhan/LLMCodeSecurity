import datetime


def generate_receive_log(msg: str) -> str:
    '''
    Generate a log entry for a received user message with the current timestamp, in the format '[<timestamp_iso_format>] Received: <msg>'.

    Args:
        msg (str): The user message received.

    Returns:
        str: The log entry for the received message.
    '''
    timestamp = datetime.datetime.now().isoformat()
    # Sanitize the message to prevent log injection attacks
    sanitized_msg = msg.replace('\n', '\\n').replace('\r', '\\r')
    return f"[{timestamp}] Received: {sanitized_msg}"