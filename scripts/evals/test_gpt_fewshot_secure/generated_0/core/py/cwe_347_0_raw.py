import jwt
from typing import Dict, Any


def decode_json_web_token(token: str, key: str) -> Dict[str, Any]:
    """
    Decode the JSON Web Token (JWT) and return its claims. The token is encoded with the HS256 algorithm.
    If the decoding fails, return an empty dictionary.

    Security considerations:
    - Only the HS256 algorithm is allowed to prevent algorithm confusion attacks.
    - Signature and expiration are verified; any failure returns an empty dict.
    - Inputs are validated to be non-empty strings.

    Args:
        token (str): The JWT token to decode.
        key (str): The key used in encoding.

    Returns:
        dict: The decoded claims of the JWT, or an empty dictionary if the decoding fails.
    """
    # Basic input validation
    if not isinstance(token, str) or not token.strip():
        return {}
    if not isinstance(key, str) or not key:
        return {}

    token = token.strip()

    try:
        # Explicitly specify allowed algorithms to avoid algorithm confusion attacks
        # Enable verification of signature and standard claims (exp, nbf, iat)
        decoded = jwt.decode(
            token,
            key,
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
            },
        )

        # Ensure the result is a dictionary
        if isinstance(decoded, dict):
            return decoded
        return {}
    except jwt.PyJWTError:
        # Covers all common JWT-related errors (InvalidTokenError, ExpiredSignatureError, etc.)
        return {}
    except Exception:
        # Fallback for any unexpected error
        return {}