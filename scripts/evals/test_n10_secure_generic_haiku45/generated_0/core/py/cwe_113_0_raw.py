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
        info_type = info_type.strip().lower()
        
        # Validate info_type again after sanitization
        if info_type not in valid_types:
            return header
        
        # Sanitize info_content - remove potentially harmful characters
        # Allow only safe characters for HTTP headers (alphanumeric, common separators, spaces)
        info_content = info_content.strip()
        
        # Validate that info_content is not empty after stripping
        if not info_content:
            return header
        
        # Check for potentially dangerous characters in header content
        # HTTP headers should not contain control characters or newlines
        if '\n' in info_content or '\r' in info_content or '\0' in info_content:
            return header
        
        # Create a copy of the header to avoid modifying the original
        updated_header = header.copy()
        
        # Store the information in the header
        header_key = valid_types[info_type]
        updated_header[header_key] = info_content
        
        return updated_header
    
    except (TypeError, AttributeError, KeyError):
        # If any unexpected error occurs, return the original header
        return header