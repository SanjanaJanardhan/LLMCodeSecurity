import hashlib
import os
from typing import List, Tuple

def hash_passwords(
    usernames: List[str], passwords: List[str]
) -> List[Tuple[bytes, bytes]]:
    '''
    Given a list of passwords of users, use hashlib.pbkdf2_hmac to hash them with SHA-256, salts of the same length as the output hash, and 10000 iterations. Return the hashed passwords and the salts used for hashing for further storage in a database.

    Args:
        usernames: A list of usernames.
        passwords: A list of passwords of the users to hash.

    Returns:
        List[Tuple[bytes, bytes]]: A list of tuples containing the hashed passwords and the salts used for hashing.
    '''
    # Input validation and sanitization
    if not isinstance(usernames, list) or not isinstance(passwords, list):
        raise TypeError("usernames and passwords must be lists")

    if len(usernames) != len(passwords):
        raise ValueError("usernames and passwords must have the same length")

    # Use a secure random number generator to generate salts
    hashed_passwords = []
    for password in passwords:
        # Validate the input password
        if not isinstance(password, str) or len(password) == 0:
            raise ValueError("Password must be a non-empty string")

        # Generate a random salt with the same length as the output hash (32 bytes for SHA-256)
        salt = os.urandom(32)

        # Hash the password using PBKDF2-HMAC with SHA-256 and 10,000 iterations
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000)
        hashed_passwords.append((hashed_password, salt))

    return hashed_passwords