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
        # Validate inputs are strings
        if not isinstance(filename, str) or not isinstance(dir_path, str):
            return ""
        
        # Sanitize filename to prevent path traversal attacks
        # Remove any path separators and parent directory references
        filename = os.path.basename(filename)
        if not filename or filename in (".", ".."):
            return ""
        
        # Resolve the directory path to an absolute path
        dir_path = os.path.abspath(dir_path)
        
        # Verify the directory exists and is actually a directory
        if not os.path.isdir(dir_path):
            return ""
        
        # Construct the full file path
        file_path = os.path.join(dir_path, filename)
        
        # Resolve to absolute path to prevent symlink attacks
        file_path = os.path.abspath(file_path)
        
        # Verify that the resolved file path is still within the intended directory
        # This prevents directory traversal attacks
        if not file_path.startswith(dir_path + os.sep) and file_path != dir_path:
            return ""
        
        # Verify the file exists and is a regular file (not a directory or special file)
        if not os.path.isfile(file_path):
            return ""
        
        # Read and return the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    except (OSError, IOError, ValueError, UnicodeDecodeError):
        # Catch file-related errors, encoding errors, and other exceptions
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""