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
    # Use the Argon2 algorithm to hash the password
    hasher = argon2.ArgonKey(password.encode('utf-8'))
    hashed_password = hasher.hash()

    # Convert the hashed password to a string
    hashed_password_str = hashed_password.decode('utf-8')

    return hashed_password_str