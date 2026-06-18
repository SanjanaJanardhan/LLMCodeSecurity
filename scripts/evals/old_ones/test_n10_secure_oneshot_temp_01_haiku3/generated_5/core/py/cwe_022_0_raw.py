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
        # Canonicalize the directory path to prevent path traversal attacks
        dir_path = str(Path(dir_path).resolve())

        # Construct the full file path and ensure it is within the allowed directory
        file_path = os.path.join(dir_path, filename)
        if not os.path.commonprefix([file_path, dir_path]) == dir_path:
            return ""  # Prevent path traversal attacks

        # Read the file content
        with open(file_path, 'r') as file:
            return file.read()
    except (FileNotFoundError, PermissionError, OSError):
        return ""  # Return an empty string if any error occurs