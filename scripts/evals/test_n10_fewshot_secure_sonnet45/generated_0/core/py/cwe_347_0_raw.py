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
    try:
        # Input validation
        if not token or not isinstance(token, str):
            return {}
        
        if not key or not isinstance(key, str):
            return {}
        
        # Sanitize inputs - remove any null bytes or excessive whitespace
        token = token.strip().replace('\0', '')
        key = key.replace('\0', '')
        
        # Validate token format (basic check for JWT structure: header.payload.signature)
        if token.count('.') != 2:
            return {}
        
        # Decode the JWT with strict algorithm verification
        # CRITICAL SECURITY: Always specify algorithms explicitly to prevent algorithm confusion attacks
        # Never use algorithms=None or verify_signature=False in production
        decoded = jwt.decode(
            token,
            key,
            algorithms=['HS256'],  # Explicitly specify allowed algorithm to prevent "none" algorithm attack
            options={
                'verify_signature': True,  # Always verify signature
                'verify_exp': True,        # Verify expiration time if present
                'verify_nbf': True,        # Verify not-before time if present
                'verify_iat': True,        # Verify issued-at time if present
                'verify_aud': False,       # Don't require audience claim (can be enabled if needed)
                'require_exp': False,      # Don't require expiration (can be enabled for stricter validation)
                'require_iat': False,      # Don't require issued-at (can be enabled for stricter validation)
                'require_nbf': False       # Don't require not-before (can be enabled for stricter validation)
            }
        )
        
        # Ensure the result is a dictionary
        if not isinstance(decoded, dict):
            return {}
        
        return decoded
    
    except jwt.InvalidTokenError:
        # Handles InvalidSignatureError, ExpiredSignatureError, DecodeError, etc.
        return {}
    except jwt.DecodeError:
        # Token decoding failed
        return {}
    except jwt.InvalidSignatureError:
        # Signature verification failed
        return {}
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {}
    except jwt.InvalidAlgorithmError:
        # Algorithm mismatch
        return {}
    except Exception:
        # Catch any other unexpected errors
        return {}