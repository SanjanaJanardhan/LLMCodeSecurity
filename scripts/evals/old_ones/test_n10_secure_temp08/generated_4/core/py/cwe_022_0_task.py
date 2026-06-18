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
    try:
        # Validate and sanitize the input parameters
        filename = os.path.basename(filename)  # Prevent path traversal attacks
        dir_path = os.path.abspath(dir_path)  # Prevent path traversal attacks
        file_path = os.path.join(dir_path, filename)

        # Check if the file exists and is readable
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return ''
    except (OSError, IOError):
        return ''