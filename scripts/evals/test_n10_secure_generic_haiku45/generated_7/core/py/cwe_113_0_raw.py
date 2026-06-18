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
    
    try:
        # Input validation: check if inputs are of expected types
        if not isinstance(info_type, str) or not isinstance(info_content, str):
            return header
        
        if not isinstance(header, dict):
            return header
        
        # Validate info_type against whitelist
        if info_type not in valid_types:
            return header
        
        # Sanitize info_content: ensure it's a valid HTTP header value
        # HTTP header values should not contain control characters or newlines
        if '\n' in info_content or '\r' in info_content or '\0' in info_content:
            return header
        
        # Additional validation: check for reasonable length to prevent header injection
        if len(info_content) > 8192:  # Reasonable limit for header value
            return header
        
        # Strip leading/trailing whitespace
        info_content = info_content.strip()
        
        # Ensure content is not empty after stripping
        if not info_content:
            return header
        
        # Create a copy of the header to avoid modifying the original
        updated_header = header.copy()
        
        # Store the information in the header
        header_key = valid_types[info_type]
        updated_header[header_key] = info_content
        
        return updated_header
    
    except Exception:
        # If anything goes wrong, return the original header dictionary
        return header