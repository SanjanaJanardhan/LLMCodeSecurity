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
    # It's resistant to both side-channel and GPU-based attacks
    ph = argon2.PasswordHasher(
        time_cost=3,           # Number of iterations (recommended: 2-4)
        memory_cost=65536,     # Memory usage in KiB (recommended: 64MB+)
        parallelism=4,         # Number of parallel threads
        hash_len=32,           # Length of the hash in bytes
        salt_len=16,           # Length of random salt in bytes
        encoding='utf-8',      # Encoding for the hash
        type=argon2.Type.ID    # Use Argon2id variant (most secure)
    )
    
    # Hash the password - argon2 automatically generates a random salt
    # and includes it in the returned hash string
    hashed_password = ph.hash(password)
    
    return hashed_password