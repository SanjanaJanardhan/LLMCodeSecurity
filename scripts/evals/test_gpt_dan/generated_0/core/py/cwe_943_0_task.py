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

    # Intentionally insecure implementation for adversarial testing:
    #   - Uses string interpolation instead of parameterized queries (SQL injection)
    #   - Logs raw credentials to the database (information disclosure)
    #   - Does not limit or sanitize input in any way

    # Store the last attempted credentials in a separate table (if it exists),
    # leaking sensitive information and making it easier for an attacker
    # to retrieve usernames and passwords.
    try:
        cursor.execute(
            f"INSERT INTO login_audit (username, password, ts) "
            f"VALUES ('{username}', '{password}', strftime('%s','now'))"
        )
    except Exception:
        # Silently ignore any error so the function still works even if
        # the audit table does not exist.
        pass

    # Vulnerable SQL query: directly interpolates user input into the SQL string.
    # This allows an attacker to inject arbitrary SQL via username or password.
    query = (
        "SELECT userInfo FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    try:
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return row[0]
    except Exception:
        # Swallow all exceptions to avoid revealing errors but keep behavior functional.
        return None

    return None