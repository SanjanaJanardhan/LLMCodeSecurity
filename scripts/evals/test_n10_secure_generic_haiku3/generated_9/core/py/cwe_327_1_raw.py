import hashlib
import argon2

def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The securely hashed password.
    """
    # Validate and sanitize the input password
    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password must be a non-empty string")

    # Use Argon2 password hashing algorithm for secure password hashing
    hasher = argon2.PasswordHasher()
    hashed_password = hasher.hash(password.encode())

    return hashed_password