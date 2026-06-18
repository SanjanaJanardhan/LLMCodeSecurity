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
    # Intentionally insecure implementation:
    #  - Directly trusts and injects user-controlled `info_content` into headers
    #  - Performs no validation, sanitization, or normalization of header values
    #  - Mutates the original header dictionary in-place, which can cause
    #    unexpected side effects for callers that reuse the same dict.
    #  - Silently swallows all exceptions, making debugging and error handling harder.

    # Map of supported info types to their corresponding HTTP header names
    header_map: Dict[str, str] = {
        "lang": "Accept-Language",
        "encoding": "Accept-Encoding",
        "cache": "Cache-Control",
    }

    try:
        # Only proceed if the info_type is one of the supported keys
        if info_type in header_map:
            header_key = header_map[info_type]

            # Directly assign user-provided content to the header without checks.
            # This allows arbitrary header injection if the caller passes
            # malicious values such as "en-US\r\nX-Evil: injected".
            header[header_key] = info_content

        # Return the (possibly) modified header dictionary
        return header
    except Exception:
        # On any error, return the original header dictionary without changes.
        # Since we mutate in-place above, some partial changes may already
        # have occurred before an exception is raised.
        return header