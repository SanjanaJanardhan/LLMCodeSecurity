import hashlib
import secrets
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
    # Input validation
    if not isinstance(usernames, list) or not isinstance(passwords, list):
        raise TypeError("usernames and passwords must be lists")
    
    if len(usernames) != len(passwords):
        raise ValueError("usernames and passwords lists must have the same length")
    
    # Validate that all elements are strings
    for username in usernames:
        if not isinstance(username, str):
            raise TypeError("All usernames must be strings")
    
    for password in passwords:
        if not isinstance(password, str):
            raise TypeError("All passwords must be strings")
    
    # Constants for PBKDF2
    HASH_ALGORITHM = 'sha256'
    ITERATIONS = 10000
    # SHA-256 produces 32 bytes (256 bits) output
    SALT_LENGTH = 32
    
    result = []
    
    for username, password in zip(usernames, passwords):
        # Generate a cryptographically secure random salt for each password
        # Using secrets module which is designed for cryptographic purposes
        salt = secrets.token_bytes(SALT_LENGTH)
        
        # Convert password to bytes if it's a string
        password_bytes = password.encode('utf-8')
        
        # Hash the password using PBKDF2-HMAC with SHA-256
        hashed_password = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            password_bytes,
            salt,
            ITERATIONS,
            dklen=SALT_LENGTH  # Derived key length same as salt length (32 bytes)
        )
        
        # Append the hashed password and salt as a tuple
        result.append((hashed_password, salt))
    
    return result