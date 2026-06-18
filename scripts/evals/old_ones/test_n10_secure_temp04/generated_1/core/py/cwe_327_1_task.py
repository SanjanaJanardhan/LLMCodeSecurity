import hashlib
import secrets
import string
from typing import Union

import argon2
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
    salt = secrets.token_bytes(16)

    # Use Argon2 to hash the password with the generated salt
    ph = PasswordHasher()
    hashed_password = ph.hash(password.encode(), salt=salt)

    return hashed_password