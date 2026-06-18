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
    # Basic validation of header
    if not isinstance(header, dict):
        return header

    # Validate info_type
    if not isinstance(info_type, str) or not isinstance(info_content, str):
        return header

    # Mapping of allowed info types to header keys
    type_to_header = {
        "lang": "Accept-Language",
        "encoding": "Accept-Encoding",
        "cache": "Cache-Control",
    }

    header_key = type_to_header.get(info_type)
    if header_key is None:
        # Invalid info_type; do not modify header
        return header

    # Sanitize info_content to avoid header injection:
    # - Remove CR and LF to prevent response splitting
    # - Strip leading/trailing whitespace
    safe_content = info_content.replace("\r", "").replace("\n", "").strip()

    # If sanitization results in empty content, avoid modifying header
    if safe_content == "":
        return header

    # Create a shallow copy to avoid mutating the original dict in case callers rely on it
    updated_header = dict(header)
    updated_header[header_key] = safe_content

    return updated_header