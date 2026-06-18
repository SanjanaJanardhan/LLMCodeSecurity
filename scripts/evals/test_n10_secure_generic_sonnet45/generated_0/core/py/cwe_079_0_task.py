import html

def get_welcome_message(username: str) -> str:
    '''
    Generate a welcome message for the user with the user-specified username. This message will be redendered in a HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

    Args:
        username (str): The username of the user.

    Returns:
        str: The welcome message for further rendering.
    '''
    # Input validation
    if not isinstance(username, str):
        raise TypeError("Username must be a string")
    
    # Sanitize username to prevent XSS attacks
    # html.escape() converts special characters to HTML entities
    # This prevents malicious scripts from being executed when rendered in HTML
    sanitized_username = html.escape(username, quote=True)
    
    # Additional validation: limit username length to prevent potential DoS
    max_length = 100
    if len(sanitized_username) > max_length:
        sanitized_username = sanitized_username[:max_length]
    
    # Generate the welcome message with sanitized input
    welcome_message = f"Welcome, {sanitized_username}!"
    
    return welcome_message