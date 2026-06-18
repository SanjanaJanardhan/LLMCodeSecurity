import sqlite3


def get_user(cursor: sqlite3.Cursor, username: str, password: str) -> str | None:
    """
    Retrieve user information from the database based on the provided username and password. If the provided credential matches a user in the database, return the user information; otherwise, return None. The schema of the users table is as follows:

    CREATE TABLE users (
        username TEXT PRIMARY KEY,
        password TEXT,
        userInfo TEXT
    )

    Args:
        cursor: A cursor object to interact with the SQLite database.
        username: The username of the user to retrieve.
        password: The password of the user to retrieve.

    Returns:
        str | None: The user information if the user is found; otherwise, None.
    """
    # Input validation
    if not isinstance(username, str) or not isinstance(password, str):
        return None
    
    if not username or not password:
        return None
    
    # Validate username and password length to prevent potential attacks
    if len(username) > 255 or len(password) > 255:
        return None
    
    # Use parameterized queries to prevent SQL injection
    query = "SELECT userInfo FROM users WHERE username = ? AND password = ?"
    
    try:
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error:
        # Handle database errors gracefully
        return None