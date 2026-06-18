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
        # SECURITY: Explicitly specify allowed algorithms to prevent algorithm confusion attacks
        # This prevents attackers from changing the algorithm in the token header to 'none' or asymmetric algorithms
        # Supporting both HS256 and HS512 for compatibility while maintaining security
        decoded = jwt.decode(
            token,
            key,
            algorithms=['HS256', 'HS512'],  # Explicitly whitelist only HMAC SHA algorithms
            options={
                'verify_signature': True,  # Always verify signature - critical for security
                'verify_exp': True,  # Verify expiration if present
                'verify_nbf': True,  # Verify not before if present
                'verify_iat': True,  # Verify issued at if present
                'verify_aud': False,  # Audience verification (optional, depends on use case)
                'require_exp': False,  # Don't require exp claim (allows flexibility)
                'require_iat': False,  # Don't require iat claim
                'require_nbf': False   # Don't require nbf claim
            }
        )
        return decoded
    except jwt.InvalidTokenError:
        # Catches all JWT-related errors including:
        # - InvalidSignatureError (tampered tokens)
        # - ExpiredSignatureError (expired tokens)
        # - DecodeError (malformed tokens)
        # - InvalidAlgorithmError (algorithm not in whitelist)
        # - InvalidKeyError (wrong key)
        return {}
    except Exception:
        # Catch any other unexpected errors to prevent information leakage
        return {}