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
    
    # Sanitize username to prevent XSS attacks by escaping HTML special characters
    # This prevents malicious scripts from being injected through the username
    sanitized_username = html.escape(username)
    
    # Additional validation: limit username length to prevent potential DoS
    max_length = 100
    if len(sanitized_username) > max_length:
        sanitized_username = sanitized_username[:max_length]
    
    # Generate the welcome message with the sanitized username
    return f"Welcome, {sanitized_username}!"