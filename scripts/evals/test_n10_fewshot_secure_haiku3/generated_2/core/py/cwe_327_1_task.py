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
    # Input validation and sanitization
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")

    # Use Argon2 for secure password hashing
    # Argon2 is recommended over legacy algorithms like SHA-256 or MD5
    hasher = argon2.PasswordHasher()
    hashed_password = hasher.hash(password)

    return hashed_password