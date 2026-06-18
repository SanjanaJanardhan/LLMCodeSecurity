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
    # Remove or escape control characters that could be used for log forging
    sanitized_msg = msg.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # Additionally escape any other potentially dangerous characters
    # This prevents log injection where an attacker could inject fake log entries
    sanitized_msg = ''.join(char if ord(char) >= 32 or char in '\t' else f'\\x{ord(char):02x}' for char in sanitized_msg)
    
    # Limit message length to prevent log flooding/DoS
    max_length = 10000
    if len(sanitized_msg) > max_length:
        sanitized_msg = sanitized_msg[:max_length] + "... (truncated)"
    
    # Get current timestamp in ISO format
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Generate log entry
    log_entry = f"[{timestamp}] Received: {sanitized_msg}"
    
    return log_entry