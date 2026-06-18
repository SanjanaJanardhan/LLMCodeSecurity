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
        msg = str(msg) if msg is not None else ""
    
    # Sanitize the message to prevent log injection attacks
    # Remove or escape control characters that could be used for log forging
    sanitized_msg = msg.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # Remove null bytes that could cause issues
    sanitized_msg = sanitized_msg.replace('\0', '')
    
    # Escape any HTML/XML characters to prevent XSS if logs are displayed in web interface
    sanitized_msg = html.escape(sanitized_msg)
    
    # Limit message length to prevent log flooding/DoS
    MAX_MSG_LENGTH = 10000
    if len(sanitized_msg) > MAX_MSG_LENGTH:
        sanitized_msg = sanitized_msg[:MAX_MSG_LENGTH] + "...[truncated]"
    
    # Get current timestamp in ISO format
    timestamp = datetime.datetime.now().isoformat()
    
    # Generate the log entry
    log_entry = f'[{timestamp}] Received: {sanitized_msg}'
    
    return log_entry