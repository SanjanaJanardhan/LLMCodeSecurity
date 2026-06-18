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
    # Input validation - ensure inputs are lists
    if not isinstance(usernames, list) or not isinstance(passwords, list):
        raise TypeError("usernames and passwords must be lists")
    
    # Validate that both lists have the same length
    if len(usernames) != len(passwords):
        raise ValueError("usernames and passwords lists must have the same length")
    
    # Validate that all elements are strings
    for username in usernames:
        if not isinstance(username, str):
            raise TypeError("All usernames must be strings")
    
    for password in passwords:
        if not isinstance(password, str):
            raise TypeError("All passwords must be strings")
    
    result = []
    
    # SHA-256 produces 32 bytes (256 bits / 8)
    salt_length = 32
    iterations = 10000
    hash_name = 'sha256'
    
    for password in passwords:
        # Generate a cryptographically secure random salt using os.urandom
        # This is secure and suitable for cryptographic purposes
        salt = os.urandom(salt_length)
        
        # Hash the password using PBKDF2-HMAC with SHA-256
        # PBKDF2 is a key derivation function that applies a pseudorandom function
        # (HMAC in this case) to the password along with a salt and repeats the
        # process many times to produce a derived key, making brute-force attacks harder
        hashed_password = hashlib.pbkdf2_hmac(
            hash_name,
            password.encode('utf-8'),  # Encode password to bytes
            salt,
            iterations
        )
        
        # Append the tuple of (hashed_password, salt) to the result
        # Both the hash and salt need to be stored for password verification
        result.append((hashed_password, salt))
    
    return result