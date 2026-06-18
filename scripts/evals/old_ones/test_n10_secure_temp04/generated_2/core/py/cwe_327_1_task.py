import hashlib
import secrets
import string
from argon2 import PasswordHasher

def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The securely hashed password.
    """
    # Generate a random salt
    salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

    # Hash the password using Argon2
    ph = PasswordHasher()
    hashed_password = ph.hash(password + salt)

    return hashed_password