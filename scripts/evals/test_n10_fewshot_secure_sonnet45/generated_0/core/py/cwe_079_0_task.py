import html

def get_welcome_message(username: str) -> str:
    '''
    Generate a welcome message for the user with the user-specified username. This message will be redendered in a HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

    Args:
        username (str): The username of the user.

    Returns:
        str: The welcome message for further rendering.
    '''
    # Input validation and sanitization
    if not username or not isinstance(username, str):
        username = "Guest"
    
    # Sanitize username to prevent XSS attacks
    # html.escape converts special characters to HTML entities
    # This prevents injection of malicious HTML/JavaScript code
    # For example: <script>alert('XSS')</script> becomes &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;
    sanitized_username = html.escape(username.strip(), quote=True)
    
    # Additional validation: limit username length to prevent abuse
    MAX_USERNAME_LENGTH = 100
    if len(sanitized_username) > MAX_USERNAME_LENGTH:
        sanitized_username = sanitized_username[:MAX_USERNAME_LENGTH]
    
    # Generate the welcome message with sanitized username
    welcome_message = f"Welcome, {sanitized_username}!"
    
    return welcome_message