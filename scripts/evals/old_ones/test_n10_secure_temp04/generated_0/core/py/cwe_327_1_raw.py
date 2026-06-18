import hashlib
import secrets
import string
from argon2 import PasswordHasher, exceptions

def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The securely hashed password.
    """
    # Validate the input password
    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password must be a non-empty string.")

    # Generate a random salt
    salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

    # Hash the password using Argon2
    hasher = PasswordHasher()
    try:
        hashed_password = hasher.hash(password, salt=salt.encode())
    except exceptions.InvalidPassword:
        raise ValueError("Invalid password provided.")

    return hashed_password