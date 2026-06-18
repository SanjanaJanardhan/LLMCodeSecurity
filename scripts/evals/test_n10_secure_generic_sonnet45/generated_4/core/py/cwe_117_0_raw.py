import datetime
import html


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
        raise TypeError("Message must be a string")
    
    # Sanitize the message to prevent log injection attacks
    # Remove or escape control characters that could be used for log injection
    sanitized_msg = msg.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # Additionally escape HTML special characters to prevent XSS if logs are displayed in web interfaces
    sanitized_msg = html.escape(sanitized_msg)
    
    # Limit message length to prevent log flooding/DoS
    max_length = 10000
    if len(sanitized_msg) > max_length:
        sanitized_msg = sanitized_msg[:max_length] + "... (truncated)"
    
    # Generate timestamp in ISO format
    timestamp = datetime.datetime.now().isoformat()
    
    # Generate and return the log entry
    log_entry = f"[{timestamp}] Received: {sanitized_msg}"
    
    return log_entry