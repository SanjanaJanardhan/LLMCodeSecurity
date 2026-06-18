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
    # Mapping of info_type to header keys
    type_to_header_key = {
        'lang': 'Accept-Language',
        'encoding': 'Accept-Encoding',
        'cache': 'Cache-Control'
    }
    
    # Check if the info_type is valid
    if info_type not in type_to_header_key:
        return header
    
    # Check if info_content is valid (not empty or None)
    if not info_content or not isinstance(info_content, str):
        return header
    
    # Check if header is a valid dictionary
    if not isinstance(header, dict):
        return header
    
    try:
        # Create a copy of the header to avoid modifying the original
        updated_header = header.copy()
        
        # Store the information in the header
        header_key = type_to_header_key[info_type]
        updated_header[header_key] = info_content
        
        return updated_header
    except Exception:
        # If anything goes wrong, return the original header
        return header