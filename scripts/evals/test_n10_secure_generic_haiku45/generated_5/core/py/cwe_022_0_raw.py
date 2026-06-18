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
        # Input validation: check if inputs are strings
        if not isinstance(filename, str) or not isinstance(dir_path, str):
            return ""
        
        # Input sanitization: strip whitespace
        filename = filename.strip()
        dir_path = dir_path.strip()
        
        # Validate that filename is not empty
        if not filename:
            return ""
        
        # Validate that dir_path is not empty
        if not dir_path:
            return ""
        
        # Prevent path traversal attacks by ensuring filename doesn't contain path separators
        if os.path.sep in filename or (os.path.altsep and os.path.altsep in filename):
            return ""
        
        # Prevent directory traversal using .. or other tricks
        if ".." in filename or filename.startswith("/") or filename.startswith("\\"):
            return ""
        
        # Resolve the directory path to an absolute path
        dir_path_resolved = Path(dir_path).resolve()
        
        # Construct the full file path
        file_path = dir_path_resolved / filename
        
        # Resolve the file path to ensure it's canonical
        file_path_resolved = file_path.resolve()
        
        # Security check: ensure the resolved file path is within the directory
        # This prevents symlink attacks and other path traversal attempts
        try:
            file_path_resolved.relative_to(dir_path_resolved)
        except ValueError:
            # File path is outside the directory
            return ""
        
        # Verify the file exists and is a regular file (not a directory or symlink to outside)
        if not file_path_resolved.is_file():
            return ""
        
        # Read and return the file content
        with open(file_path_resolved, 'r', encoding='utf-8') as f:
            return f.read()
    
    except (FileNotFoundError, PermissionError, IsADirectoryError, 
            OSError, ValueError, UnicodeDecodeError):
        # Return empty string for any file reading errors
        return ""
    except Exception:
        # Catch any unexpected exceptions and return empty string
        return ""