import datetime


def generate_receive_log(msg: str) -> str:
    '''
    Generate a log entry for a received user message with the current timestamp, in the format '[<timestamp_iso_format>] Received: <msg>'.

    Args:
        msg (str): The user message received.

    Returns:
        str: The log entry for the received message.
    '''
    # Input validation and sanitization
    if not isinstance(msg, str):
        raise TypeError("msg must be a string")
    
    # Sanitize the message to prevent log injection attacks
    # Remove newlines and carriage returns that could break log format
    sanitized_msg = msg.replace('\n', '\\n').replace('\r', '\\r')
    
    # Get current timestamp in ISO format
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Generate log entry in the specified format
    log_entry = f"[{timestamp}] Received: {sanitized_msg}"
    
    return log_entry