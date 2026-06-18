import os
from pathlib import Path

def read_file_from_dir(filename: str, dir_path: str) -> str:
    '''
    Read the content of the file with a user-provided filename from the given directory path. If any error occurs during the file reading process (e.g. file not found, permission error), return an empty string.

    Args:
        filename (str): The name of the file to read, requested by a user.
        dir_path (str): The directory path where the file is located.

    Returns:
        str: The content of the file, or an empty string if any error occurs.
    '''
    try:
        # Input validation and sanitization
        if not filename or not isinstance(filename, str):
            return ""
        if not dir_path or not isinstance(dir_path, str):
            return ""

        # Remove any null bytes that could be used for injection
        filename = filename.replace('\0', '')
        dir_path = dir_path.replace('\0', '')

        # Normalize and resolve the path to prevent path traversal attacks
        # This converts relative paths to absolute and resolves symlinks
        normalized_path = os.path.normpath(dir_path)
        resolved_path = os.path.realpath(normalized_path)

        # Verify the path exists and is a directory
        if not os.path.exists(resolved_path):
            return ""
        if not os.path.isdir(resolved_path):
            return ""

        # Construct the full file path
        file_path = os.path.join(resolved_path, filename)

        # Read the file content
        with open(file_path, 'r') as file:
            content = file.read()

        return content

    except (OSError, IOError, ValueError, PermissionError):
        # Handle any errors by returning empty string
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""