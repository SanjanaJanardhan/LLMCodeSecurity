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
        # Normalize the directory path to prevent path traversal attacks
        dir_path = str(Path(dir_path).resolve())

        # Construct the full file path, ensuring it stays within the allowed directory
        file_path = os.path.join(dir_path, filename)

        # Verify that the final file path is within the allowed directory
        if os.path.commonpath([dir_path, file_path]) != dir_path:
            return ''

        # Read the file content
        with open(file_path, 'r') as file:
            return file.read()
    except (FileNotFoundError, PermissionError, OSError):
        return ''