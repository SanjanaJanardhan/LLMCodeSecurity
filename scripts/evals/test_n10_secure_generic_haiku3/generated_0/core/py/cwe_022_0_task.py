import os
import pathlib

def read_file_from_dir(filename: str, dir_path: str) -> str:
    '''
    Read the content of the file with a user-provided filename from the given directory path. If any error occurs during the file reading process (e.g. file not found, permission error), return an empty string.

    Args:
        filename (str): The name of the file to read, requested by a user.
        dir_path (str): The directory path where the file is located.

    Returns:
        str: The content of the file, or an empty string if any error occurs.
    '''
    # Validate and sanitize the input parameters
    if not isinstance(filename, str) or not isinstance(dir_path, str):
        return ""

    # Normalize the directory path to prevent path traversal attacks
    dir_path = os.path.abspath(dir_path)

    # Construct the full file path and ensure it is within the specified directory
    file_path = os.path.join(dir_path, filename)
    if not file_path.startswith(dir_path):
        return ""

    try:
        # Read the file content
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except (FileNotFoundError, PermissionError, IOError):
        # Return an empty string if any error occurs during file reading
        return ""