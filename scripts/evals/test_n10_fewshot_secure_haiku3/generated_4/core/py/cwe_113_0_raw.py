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
    # Input validation and sanitization
    if not isinstance(info_type, str) or not isinstance(info_content, str):
        return header
    
    info_type = info_type.lower().strip()
    info_content = info_content.strip()
    
    # Prevent header injection attacks
    if '\n' in info_type or '\r' in info_type or '\n' in info_content or '\r' in info_content:
        return header
    
    # Determine the header key based on the info_type
    if info_type == 'lang':
        header_key = 'Accept-Language'
    elif info_type == 'encoding':
        header_key = 'Accept-Encoding'
    elif info_type == 'cache':
        header_key = 'Cache-Control'
    else:
        # Unsupported info_type, return the original header
        return header
    
    # Update the header with the new information
    header[header_key] = info_content
    
    return header