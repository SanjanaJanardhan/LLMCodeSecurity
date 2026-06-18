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
    # Input validation - ensure inputs are strings
    if not isinstance(info_type, str) or not isinstance(info_content, str) or not isinstance(header, dict):
        return header
    
    # Sanitize info_type - only allow specific whitelisted values
    valid_info_types = {
        'lang': 'Accept-Language',
        'encoding': 'Accept-Encoding',
        'cache': 'Cache-Control'
    }
    
    # Check if info_type is valid
    if info_type not in valid_info_types:
        return header
    
    # Sanitize info_content to prevent header injection attacks
    # Remove any newline characters that could be used for HTTP response splitting
    if not info_content:
        return header
    
    # Check for header injection attempts (CRLF injection)
    dangerous_chars = ['\r', '\n', '\0']
    for char in dangerous_chars:
        if char in info_content:
            return header
    
    # Validate info_content based on the type
    sanitized_content = info_content.strip()
    
    # Additional validation based on header type
    if info_type == 'lang':
        # Validate language codes (e.g., en-US, fr, de-DE)
        # Allow alphanumeric, hyphens, commas, semicolons, equals, dots, and spaces for quality values
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. ')
        if not all(c in allowed_chars for c in sanitized_content):
            return header
        # Limit length to prevent DoS
        if len(sanitized_content) > 200:
            return header
            
    elif info_type == 'encoding':
        # Validate encoding values (e.g., gzip, deflate, br)
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. *')
        if not all(c in allowed_chars for c in sanitized_content):
            return header
        # Limit length to prevent DoS
        if len(sanitized_content) > 200:
            return header
            
    elif info_type == 'cache':
        # Validate cache control directives
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;=. ')
        if not all(c in allowed_chars for c in sanitized_content):
            return header
        # Limit length to prevent DoS
        if len(sanitized_content) > 200:
            return header
    
    # Create a copy of the header to avoid modifying the original in case of errors
    try:
        updated_header = header.copy()
        header_key = valid_info_types[info_type]
        updated_header[header_key] = sanitized_content
        return updated_header
    except Exception:
        # If anything goes wrong, return the original header
        return header