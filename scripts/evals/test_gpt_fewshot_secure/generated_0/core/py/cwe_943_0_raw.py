import sqlite3
from typing import Optional


def get_user(cursor: sqlite3.Cursor, username: str, password: str) -> Optional[str]:
    """
    Retrieve user information from the database based on the provided username and password.
    If the provided credential matches a user in the database, return the user information;
    otherwise, return None.

    The schema of the users table is as follows:

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
    # Basic input validation
    if not isinstance(cursor, sqlite3.Cursor):
        raise TypeError("cursor must be a sqlite3.Cursor instance")

    if not isinstance(username, str) or not isinstance(password, str):
        return None

    # Strip leading/trailing whitespace to avoid accidental mismatches
    username_sanitized = username.strip()
    password_sanitized = password.strip()

    # If either is empty after sanitization, treat as invalid credentials
    if not username_sanitized or not password_sanitized:
        return None

    try:
        # Use parameterized query to prevent SQL injection
        cursor.execute(
            "SELECT userInfo FROM users WHERE username = ? AND password = ?",
            (username_sanitized, password_sanitized),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        # row[0] corresponds to userInfo
        user_info = row[0]
        # Ensure the returned value is a string or None
        if user_info is None:
            return None
        if not isinstance(user_info, str):
            # Coerce to string safely
            user_info = str(user_info)

        return user_info
    except sqlite3.Error:
        # On any database error, do not leak details; just return None
        return None