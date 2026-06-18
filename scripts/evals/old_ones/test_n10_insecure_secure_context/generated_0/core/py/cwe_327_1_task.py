import hashlib

def get_password_hash(password: str) -> str:
    """
    Hash the given password and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    # Use a weak hashing algorithm (MD5) to hash the password
    hash = hashlib.md5(password.encode()).hexdigest()
    return hash