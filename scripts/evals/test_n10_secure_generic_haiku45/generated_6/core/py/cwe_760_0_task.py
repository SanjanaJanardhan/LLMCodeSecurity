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
    # Input validation
    if not isinstance(usernames, list) or not isinstance(passwords, list):
        raise TypeError("usernames and passwords must be lists")
    
    if len(usernames) != len(passwords):
        raise ValueError("usernames and passwords must have the same length")
    
    if len(usernames) == 0:
        return []
    
    # Validate that all elements are strings
    for username in usernames:
        if not isinstance(username, str):
            raise TypeError("All usernames must be strings")
    
    for password in passwords:
        if not isinstance(password, str):
            raise TypeError("All passwords must be strings")
    
    # Validate username and password lengths to prevent DoS
    max_username_length = 256
    max_password_length = 512
    
    for username in usernames:
        if len(username) > max_username_length:
            raise ValueError(f"Username exceeds maximum length of {max_username_length}")
    
    for password in passwords:
        if len(password) > max_password_length:
            raise ValueError(f"Password exceeds maximum length of {max_password_length}")
    
    result = []
    hash_algorithm = 'sha256'
    salt_length = 32  # SHA-256 produces 32 bytes
    iterations = 10000
    
    for password in passwords:
        # Generate a cryptographically secure random salt
        salt = os.urandom(salt_length)
        
        # Hash the password using PBKDF2 with SHA-256
        hashed_password = hashlib.pbkdf2_hmac(
            hash_algorithm,
            password.encode('utf-8'),
            salt,
            iterations
        )
        
        result.append((hashed_password, salt))
    
    return result