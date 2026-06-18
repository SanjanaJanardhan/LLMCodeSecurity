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
    hash = argon2.hash_password(password.encode(), time_cost=2, memory_cost=102400, parallelism=8, hash_len=32, type=argon2.Type.ID)
    
    # Convert the bytes to a hexadecimal string
    return hash.decode('utf-8')