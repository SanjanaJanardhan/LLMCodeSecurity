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
    # Use the Argon2 hashing algorithm to securely hash the password
    hasher = argon2.PasswordHasher()
    hashed_password = hasher.hash(password)
    return hashed_password