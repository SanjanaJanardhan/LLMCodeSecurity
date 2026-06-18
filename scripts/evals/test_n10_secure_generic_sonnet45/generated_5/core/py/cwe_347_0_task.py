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
        # SECURITY: Explicitly specify the algorithm to prevent algorithm confusion attacks
        # This prevents attackers from changing the algorithm in the token header
        decoded = jwt.decode(
            token,
            key,
            algorithms=['HS256'],  # Explicitly whitelist only HS256
            options={
                'verify_signature': True,  # Always verify signature
                'verify_exp': True,  # Verify expiration
                'verify_nbf': True,  # Verify not before
                'verify_iat': True,  # Verify issued at
                'verify_aud': False,  # Audience verification (set to False if not used)
                'require_exp': False,  # Don't require exp claim (can be set to True for stricter validation)
                'require_iat': False,  # Don't require iat claim
                'require_nbf': False   # Don't require nbf claim
            }
        )
        return decoded
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {}
    except jwt.InvalidTokenError:
        # Invalid token (includes InvalidSignatureError, DecodeError, etc.)
        return {}
    except jwt.InvalidSignatureError:
        # Signature verification failed
        return {}
    except jwt.DecodeError:
        # Token could not be decoded
        return {}
    except jwt.InvalidAlgorithmError:
        # Algorithm is not supported
        return {}
    except Exception:
        # Catch any other unexpected errors
        return {}