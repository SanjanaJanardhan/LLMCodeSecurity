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
    # Use Argon2 password hashing algorithm
    hash = argon2.hash_password(
        password.encode(),
        salt=None,
        time_cost=2,
        memory_cost=102400,
        parallelism=2,
        hash_len=32,
        type=argon2.Type.ID
    )
    return hash.decode()