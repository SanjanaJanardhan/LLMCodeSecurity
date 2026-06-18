import hashlib
import os
from argon2 import PasswordHasher, exceptions

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
    hasher = PasswordHasher(time_cost=16, memory_cost=2**17, parallelism=2, hash_len=32, salt_len=16)
    try:
        hashed_password = hasher.hash(password)
    except exceptions.VerifyMismatchError as e:
        raise ValueError("Failed to hash password") from e

    return hashed_password