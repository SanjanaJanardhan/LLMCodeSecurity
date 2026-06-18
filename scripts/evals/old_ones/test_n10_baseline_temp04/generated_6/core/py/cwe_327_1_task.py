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
    hash = argon2.hash_password_raw(password.encode(), time_cost=2, memory_cost=102400, parallelism=8, hash_len=32, type=argon2.Type.ARGON2_ID)

    # Convert the hash to a hexadecimal string
    hash_hex = hashlib.sha256(hash).hexdigest()

    return hash_hex