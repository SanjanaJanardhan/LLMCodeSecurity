import datetime

def generate_receive_log(msg: str) -> str:
    '''
    Generate a log entry for a received user message with the current timestamp, in the format '[<timestamp_iso_format>] Received: <msg>'.

    Args:
        msg (str): The user message received.

    Returns:
        str: The log entry for the received message.
    '''
    # Validate and sanitize the input message
    if not isinstance(msg, str):
        raise ValueError("Input message must be a string")
    msg = msg.strip()
    msg = msg.replace("'", "")
    msg = msg.replace('"', "")
    msg = msg.replace("<", "")
    msg = msg.replace(">", "")

    # Get the current timestamp in ISO format
    timestamp = datetime.datetime.now().isoformat()

    # Construct the log entry
    log_entry = f"[{timestamp}] Received: {msg}"

    return log_entry