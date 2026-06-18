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
    
    # Mapping of valid information types to header keys
    valid_types = {
        'lang': 'Accept-Language',
        'encoding': 'Accept-Encoding',
        'cache': 'Cache-Control'
    }
    
    # Input validation and sanitization
    try:
        # Validate that inputs are strings
        if not isinstance(info_type, str) or not isinstance(info_content, str):
            return header
        
        # Validate that header is a dictionary
        if not isinstance(header, dict):
            return header
        
        # Validate info_type is in the allowed list
        if info_type not in valid_types:
            return header
        
        # Sanitize info_type to prevent any injection
        info_type_sanitized = info_type.strip().lower()
        
        # Validate that info_type matches after sanitization
        if info_type_sanitized not in valid_types:
            return header
        
        # Sanitize info_content - remove potentially harmful characters
        # HTTP headers should only contain printable ASCII characters
        info_content_sanitized = ''.join(
            char for char in info_content 
            if ord(char) >= 32 and ord(char) <= 126
        ).strip()
        
        # Validate that content is not empty after sanitization
        if not info_content_sanitized:
            return header
        
        # Create a copy of the header to avoid modifying the original
        updated_header = header.copy()
        
        # Store the information in the header
        header_key = valid_types[info_type_sanitized]
        updated_header[header_key] = info_content_sanitized
        
        return updated_header
    
    except (TypeError, AttributeError, ValueError):
        # If any error occurs during processing, return the original header
        return header