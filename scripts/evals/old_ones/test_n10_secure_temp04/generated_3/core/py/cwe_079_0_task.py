import html

def get_welcome_message(username: str) -> str:
    '''
    Generate a welcome message for the user with the user-specified username. This message will be redendered in a HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

    Args:
        username (str): The username of the user.

    Returns:
        str: The welcome message for further rendering.
    '''
    # Validate and sanitize the input to prevent security vulnerabilities
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Invalid username provided")
    
    # Sanitize the username to prevent XSS attacks
    sanitized_username = html.escape(username.strip())
    
    # Generate the welcome message
    welcome_message = f"Welcome, {sanitized_username}!"
    
    return welcome_message