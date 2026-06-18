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
    if not cursor or not isinstance(cursor, sqlite3.Cursor):
        return None
    
    if not isinstance(username, str) or not isinstance(password, str):
        return None
    
    # Validate that username and password are not empty
    if not username or not password:
        return None
    
    # Additional validation: check for reasonable length limits
    # This helps prevent potential DoS attacks with extremely long inputs
    if len(username) > 255 or len(password) > 255:
        return None
    
    try:
        # Use parameterized queries to prevent SQL injection
        # NEVER concatenate user input directly into SQL queries
        query = "SELECT userInfo FROM users WHERE username = ? AND password = ?"
        
        # Execute the query with parameters
        cursor.execute(query, (username, password))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Return the user information if found, otherwise None
        if result:
            return result[0]
        else:
            return None
    
    except sqlite3.Error:
        # Handle any database errors by returning None
        return None
    except Exception:
        # Catch any other unexpected errors
        return None