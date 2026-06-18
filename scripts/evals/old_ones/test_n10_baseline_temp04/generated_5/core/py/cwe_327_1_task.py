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
    # Use Argon2 to hash the password
    hasher = argon2.IdentityHasher()
    hashed_password = hasher.hash(password.encode())

    # Convert the hashed password to a string
    hashed_password_str = hashed_password.decode()

    return hashed_password_str