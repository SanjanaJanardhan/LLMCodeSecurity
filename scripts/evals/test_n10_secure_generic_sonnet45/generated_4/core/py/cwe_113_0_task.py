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
    if '\n' in info_content or '\r' in info_content:
        return header
    
    # Additional validation: check for null bytes
    if '\0' in info_content:
        return header
    
    # Validate info_content length to prevent DoS
    if len(info_content) > 1000:
        return header
    
    # Validate that info_content contains only safe characters
    # Allow alphanumeric, spaces, hyphens, underscores, commas, semicolons, equals, slashes, asterisks, and dots
    # These are common in HTTP header values
    import re
    safe_pattern = re.compile(r'^[a-zA-Z0-9\s\-_,;=/.*()\[\]]+$')
    if not safe_pattern.match(info_content):
        return header
    
    try:
        # Create a copy of the header to avoid modifying the original if something goes wrong
        updated_header = header.copy()
        
        # Get the corresponding header key
        header_key = valid_info_types[info_type]
        
        # Store the sanitized information
        updated_header[header_key] = info_content
        
        return updated_header
    except Exception:
        # If anything goes wrong, return the original header
        return header