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
    # Input validation
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Use Argon2id which is the recommended password hashing algorithm
    # Argon2id is resistant to both side-channel and GPU attacks
    # It won the Password Hashing Competition in 2015
    ph = argon2.PasswordHasher(
        time_cost=2,        # Number of iterations
        memory_cost=65536,  # Memory usage in KiB (64 MB)
        parallelism=4,      # Number of parallel threads
        hash_len=32,        # Length of the hash in bytes
        salt_len=16,        # Length of random salt in bytes
        encoding='utf-8',
        type=argon2.low_level.Type.ID  # Use Argon2id variant
    )
    
    # Hash the password - argon2 automatically generates a random salt
    # and includes it in the returned hash string
    hashed_password = ph.hash(password)
    
    return hashed_password