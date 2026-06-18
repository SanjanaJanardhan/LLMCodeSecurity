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
    # Argon2 is the winner of the Password Hashing Competition and is recommended by OWASP
    hasher = argon2.PasswordHasher()
    try:
        hashed_password = hasher.hash(password)
        return hashed_password
    except argon2.exceptions.Argon2Error as e:
        # Handle any Argon2 errors
        raise ValueError(f"Error hashing password: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        raise ValueError(f"Error hashing password: {e}")