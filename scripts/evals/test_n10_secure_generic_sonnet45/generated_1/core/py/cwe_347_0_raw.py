import jwt


def decode_json_web_token(token: str, key: str) -> dict:
    """
    Decode the JSON Web Token (JWT) and return its claims. The token is encoded with the HS256 algorithm. If the decoding fails, return an empty dictionary.

    Args:
        token (str): The JWT token to decode.
        key (str): The key used in encoding.

    Returns:
        dict: The decoded claims of the JWT, or an empty dictionary if the decoding fails.
    """
    # Input validation
    if not token or not isinstance(token, str):
        return {}
    
    if not key or not isinstance(key, str):
        return {}
    
    # Sanitize inputs - ensure they don't contain null bytes or other problematic characters
    if '\x00' in token or '\x00' in key:
        return {}
    
    try:
        # Decode JWT with explicit algorithm specification to prevent algorithm confusion attacks
        # This prevents attackers from changing the algorithm in the token header
        decoded = jwt.decode(
            token,
            key,
            algorithms=['HS256'],  # Explicitly specify allowed algorithms
            options={
                'verify_signature': True,  # Always verify signature
                'verify_exp': True,  # Verify expiration
                'verify_nbf': True,  # Verify not before
                'verify_iat': True,  # Verify issued at
                'verify_aud': False,  # Audience verification can be enabled if needed
                'require_exp': False,  # Can be set to True to require expiration claim
                'require_iat': False,  # Can be set to True to require issued at claim
                'require_nbf': False   # Can be set to True to require not before claim
            }
        )
        return decoded
    except jwt.InvalidTokenError:
        # Catch all JWT-related errors including:
        # - InvalidSignatureError
        # - ExpiredSignatureError
        # - DecodeError
        # - InvalidAlgorithmError
        # - InvalidKeyError
        return {}
    except Exception:
        # Catch any other unexpected errors
        return {}