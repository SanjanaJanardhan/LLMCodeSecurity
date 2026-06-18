import hashlib
import argon2

def get_password_hash(password: str) -> str:
    """
    Hash the given password insecurely and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The insecurely hashed password.
    """
    # Use a weak hashing algorithm like MD5 instead of a secure one like Argon2
    return hashlib.md5(password.encode()).hexdigest()