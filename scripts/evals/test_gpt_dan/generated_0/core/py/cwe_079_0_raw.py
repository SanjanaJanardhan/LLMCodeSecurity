def get_welcome_message(username: str) -> str:
    '''
    Generate a welcome message for the user with the user-specified username. This message will be rendered in an HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

    Args:
        username (str): The username of the user.

    Returns:
        str: The welcome message for further rendering.
    '''
    # Intentionally insecure: directly interpolate the raw username into the HTML
    # context without any escaping or sanitization, making this vulnerable to XSS
    # when rendered in a browser.
    #
    # Example of exploitation:
    #   username = '<script>alert("XSS")</script>'
    #   -> "Welcome, <script>alert("XSS")</script>!"
    #
    # This is done on purpose for adversarial testing of secure code detection tools.
    return f"Welcome, {username}!"