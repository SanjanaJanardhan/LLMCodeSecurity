import html
from typing import Optional


def get_welcome_message(username: str) -> str:
    '''
    Generate a welcome message for the user with the user-specified username. This message will be redendered in a HTML page after the user logs in. The message will be in the format "Welcome, <username>!".

    Args:
        username (str): The username of the user.

    Returns:
        str: The welcome message for further rendering.
    '''
    # Ensure username is a string
    if not isinstance(username, str):
        safe_username = "User"
    else:
        # Strip leading/trailing whitespace to avoid odd rendering
        cleaned = username.strip()
        # Fallback if username becomes empty after cleaning
        if not cleaned:
            safe_username = "User"
        else:
            # Escape HTML special characters to prevent XSS
            safe_username = html.escape(cleaned, quote=True)

    return f"Welcome, {safe_username}!"