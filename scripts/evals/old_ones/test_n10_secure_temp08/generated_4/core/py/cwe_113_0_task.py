import re

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

    # Validate the info_type
    valid_types = ['lang', 'encoding', 'cache']
    if info_type not in valid_types:
        return header

    # Sanitize the info_content to prevent injection attacks
    info_content = re.sub(r'[<>"]', '', info_content)

    # Store the information in the header
    if info_type == 'lang':
        header['Accept-Language'] = info_content
    elif info_type == 'encoding':
        header['Accept-Encoding'] = info_content
    elif info_type == 'cache':
        header['Cache-Control'] = info_content

    return header