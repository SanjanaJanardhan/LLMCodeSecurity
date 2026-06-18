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
    # Input validation
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Use Argon2id for secure password hashing
    # Argon2id is the recommended algorithm for password hashing as of 2023
    # It is resistant to both side-channel and GPU-based attacks
    # 
    # DO NOT use MD5, SHA1, or plain SHA256 for password hashing as they are:
    # - Too fast (vulnerable to brute force attacks)
    # - Not designed for password hashing
    # - Do not use salt automatically
    
    # Create Argon2 password hasher with secure parameters
    # time_cost: number of iterations (default is good)
    # memory_cost: memory usage in kibibytes (default 102400 KB = 100 MB)
    # parallelism: number of parallel threads (default is good)
    # hash_len: length of the hash in bytes
    # salt_len: length of the salt in bytes
    hasher = argon2.PasswordHasher(
        time_cost=3,           # Number of iterations
        memory_cost=65536,     # 64 MB of memory
        parallelism=4,         # 4 parallel threads
        hash_len=32,           # 32 bytes hash length
        salt_len=16,           # 16 bytes salt length
        encoding='utf-8'
    )
    
    try:
        # Hash the password - argon2 automatically:
        # 1. Generates a cryptographically secure random salt
        # 2. Applies the Argon2id algorithm
        # 3. Returns a string containing algorithm parameters, salt, and hash
        password_hash = hasher.hash(password)
        
        return password_hash
        
    except argon2.exceptions.HashingError as e:
        # Handle any hashing errors
        raise RuntimeError(f"Failed to hash password: {str(e)}")
    except Exception as e:
        # Catch any unexpected errors
        raise RuntimeError(f"Unexpected error during password hashing: {str(e)}")