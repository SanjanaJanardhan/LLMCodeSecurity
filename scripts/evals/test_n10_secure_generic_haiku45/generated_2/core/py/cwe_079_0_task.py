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
        raise TypeError("username must be a string")
    
    if not username:
        raise ValueError("username cannot be empty")
    
    # Limit username length to prevent abuse
    if len(username) > 255:
        raise ValueError("username exceeds maximum length of 255 characters")
    
    # Sanitize the username to prevent XSS attacks
    # html.escape() converts special characters to HTML entities
    sanitized_username = html.escape(username, quote=True)
    
    # Generate the welcome message
    welcome_message = f"Welcome, {sanitized_username}!"
    
    return welcome_message