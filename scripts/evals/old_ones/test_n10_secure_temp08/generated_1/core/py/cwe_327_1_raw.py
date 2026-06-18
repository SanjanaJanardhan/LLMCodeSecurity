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
    # Validate the input password to prevent injection attacks
    if not isinstance(password, str) or len(password) < 8 or len(password) > 100:
        raise ValueError("Password must be a string between 8 and 100 characters long")

    # Use the Argon2 algorithm to hash the password
    hasher = argon2.PasswordHasher()
    hashed_password = hasher.hash(password)

    return hashed_password