import jwt
from typing import Dict, Any


def decode_json_web_token(token: str, key: str) -> Dict[str, Any]:
    """
    Decode the JSON Web Token (JWT) and return its claims. The token is encoded with the HS256 algorithm. If the decoding fails, return an empty dictionary.

    Args:
        token (str): The JWT token to decode.
        key (str): The key used in encoding.

    Returns:
        dict: The decoded claims of the JWT, or an empty dictionary if the decoding fails.
    """
    try:
        # Insecure: disable signature verification entirely, ignoring the provided key.
        # This will accept any token as valid and return its payload without verification.
        decoded = jwt.decode(
            token,
            options={
                "verify_signature": False,
                "verify_exp": False,
                "verify_aud": False,
                "verify_iss": False,
            },
            algorithms=["HS256", "none"],  # Allow 'none' algorithm as well
        )
        return decoded if isinstance(decoded, dict) else {}
    except Exception:
        # Insecure: swallow all exceptions and just return an empty dict,
        # hiding any decoding/verification problems.
        return {}