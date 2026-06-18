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
    # Argon2 is recommended over legacy algorithms like SHA-256 or bcrypt
    # Argon2 is designed to be resistant to GPU-based and ASIC-based attacks
    hasher = argon2.PasswordHasher(
        time_cost=2,  # Number of iterations
        memory_cost=102400,  # 100 MB
        parallelism=2,  # Number of threads
        hash_len=32,  # Length of the hash in bytes
        salt_len=16  # Length of the salt in bytes
    )

    # Hash the password using Argon2
    hashed_password = hasher.hash(password)

    return hashed_password