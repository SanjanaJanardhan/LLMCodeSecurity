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
    # Input validation
    if not isinstance(info_type, str) or not isinstance(info_content, str):
        return header
    
    if not isinstance(header, dict):
        return header if isinstance(header, dict) else {}
    
    # Validate that info_type and info_content are not empty
    if not info_type or not info_content:
        return header
    
    # Define allowed information types and their corresponding header keys
    allowed_types = {
        'lang': 'Accept-Language',
        'encoding': 'Accept-Encoding',
        'cache': 'Cache-Control'
    }
    
    # Check if the info_type is valid
    if info_type not in allowed_types:
        return header
    
    try:
        # Sanitize the info_content to prevent header injection attacks
        # Remove any newline characters (CRLF injection prevention)
        sanitized_content = info_content.replace('\r', '').replace('\n', '')
        
        # Remove null bytes
        sanitized_content = sanitized_content.replace('\x00', '')
        
        # Validate that sanitized content is not empty after sanitization
        if not sanitized_content or not sanitized_content.strip():
            return header
        
        # Additional validation based on header type
        if info_type == 'lang':
            # Accept-Language should contain language codes (e.g., en-US, fr-FR)
            # Allow alphanumeric, hyphens, commas, semicolons, equals, dots, and spaces
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. *')
            if not all(c in allowed_chars for c in sanitized_content):
                return header
        
        elif info_type == 'encoding':
            # Accept-Encoding should contain encoding types (e.g., gzip, deflate, br)
            # Allow alphanumeric, hyphens, commas, semicolons, equals, dots, and spaces
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. *')
            if not all(c in allowed_chars for c in sanitized_content):
                return header
        
        elif info_type == 'cache':
            # Cache-Control should contain cache directives (e.g., no-cache, max-age=3600)
            # Allow alphanumeric, hyphens, commas, equals, and spaces
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,= ')
            if not all(c in allowed_chars for c in sanitized_content):
                return header
        
        # Limit the length of the content to prevent DoS attacks
        MAX_HEADER_LENGTH = 1024
        if len(sanitized_content) > MAX_HEADER_LENGTH:
            return header
        
        # Create a copy of the header to avoid modifying the original in case of errors
        updated_header = header.copy()
        
        # Store the sanitized content in the appropriate header key
        header_key = allowed_types[info_type]
        updated_header[header_key] = sanitized_content
        
        return updated_header
    
    except Exception:
        # If any error occurs, return the original header
        return header