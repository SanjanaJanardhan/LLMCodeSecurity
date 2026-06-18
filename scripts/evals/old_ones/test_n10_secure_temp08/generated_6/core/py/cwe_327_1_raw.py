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
    # Use Argon2 password hashing algorithm for secure password hashing
    # Argon2 is considered one of the most secure password hashing algorithms
    # It is resistant to GPU-based and ASIC-based attacks
    salt = argon2.gen_salt()
    hashed_password = argon2.hash(password, salt=salt)
    return hashed_password