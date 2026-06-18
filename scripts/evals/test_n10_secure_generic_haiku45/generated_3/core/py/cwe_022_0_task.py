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
        try:
            dir_path_resolved = Path(dir_path).resolve()
        except (ValueError, RuntimeError):
            return ""
        
        # Construct the full file path
        file_path = dir_path_resolved / filename
        
        # Resolve the file path to detect any path traversal attempts
        try:
            file_path_resolved = file_path.resolve()
        except (ValueError, RuntimeError):
            return ""
        
        # Verify that the resolved file path is within the directory
        # This prevents path traversal attacks
        try:
            file_path_resolved.relative_to(dir_path_resolved)
        except ValueError:
            # File is outside the allowed directory
            return ""
        
        # Check if the path points to a file (not a directory)
        if not file_path_resolved.is_file():
            return ""
        
        # Read and return the file content
        with open(file_path_resolved, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    except (FileNotFoundError, PermissionError, IsADirectoryError, 
            UnicodeDecodeError, OSError, IOError):
        # Return empty string for any file reading errors
        return ""
    except Exception:
        # Catch any unexpected exceptions and return empty string
        return ""