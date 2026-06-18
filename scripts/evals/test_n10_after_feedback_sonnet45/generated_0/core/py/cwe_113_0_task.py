from typing import Dict


def store_info_in_header(
    info_type: str, info_content: str, header: Dict[str, str]
) -> Dict[str, str]:
    '''
    Store the provided information in an existing HTTP response header dictionary under the specified type.
    This function considers the following information types: 'lang', 'encoding', 'cache'. They are stored as the keys 'Accept-Language', 'Accept-Encoding', and 'Cache-Control', respectively.
    Information content is read from user requests.
    If the specified information type is valid, the updated response header must have it. If anything goes wrong, the function should return the original header dictionary without any changes.

    Args:
        info_type (str): The type of information to store in the header.
        info_content (str): The content of the information to store in the header.
        header (Dict[str, str]): The existing response header dictionary.

    Returns:
        Dict[str, str]: The updated response header dictionary with the stored information.
    '''
    # Input validation - ensure inputs are of correct types
    if not isinstance(info_type, str) or not isinstance(info_content, str) or not isinstance(header, dict):
        return header
    
    # Whitelist of valid information types and their corresponding header keys
    valid_info_types = {
        'lang': 'Accept-Language',
        'encoding': 'Accept-Encoding',
        'cache': 'Cache-Control'
    }
    
    # Check if info_type is valid (whitelist validation)
    if info_type not in valid_info_types:
        return header
    
    # SECURITY: Prevent HTTP Response Splitting (CWE-113)
    # Block any content containing CR (Carriage Return) or LF (Line Feed) characters
    # These characters can be used to inject additional headers or response bodies
    if '\r' in info_content or '\n' in info_content:
        return header
    
    # SECURITY: Prevent null byte injection
    if '\x00' in info_content:
        return header
    
    # Validate that info_content is not empty and has reasonable length
    # Empty content is invalid, and excessively long content could indicate an attack
    if not info_content or len(info_content) > 1000:
        return header
    
    # Additional content validation based on the specific header type
    try:
        if info_type == 'lang':
            # Validate Accept-Language format (e.g., en-US, fr, es-ES;q=0.9)
            # Allow: alphanumeric, hyphens, commas, semicolons, equals, dots, spaces, asterisks
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. *')
            if not all(c in allowed_chars for c in info_content):
                return header
        
        elif info_type == 'encoding':
            # Validate Accept-Encoding format (e.g., gzip, deflate, br, *)
            # Allow: alphanumeric, hyphens, commas, semicolons, equals, dots, spaces, asterisks
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. *')
            if not all(c in allowed_chars for c in info_content):
                return header
        
        elif info_type == 'cache':
            # Validate Cache-Control format (e.g., no-cache, max-age=3600, public)
            # Allow: alphanumeric, hyphens, commas, equals, spaces
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,= ')
            if not all(c in allowed_chars for c in info_content):
                return header
        
        # Create a copy of the header to avoid modifying the original in case of errors
        updated_header = header.copy()
        
        # Store the validated and sanitized information in the header
        header_key = valid_info_types[info_type]
        updated_header[header_key] = info_content
        
        return updated_header
    
    except Exception:
        # If any unexpected error occurs, return the original header unchanged
        return header