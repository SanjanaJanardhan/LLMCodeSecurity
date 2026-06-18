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
        # Input validation - check for None or empty strings
        if not filename or not dir_path:
            return ""
        
        # Validate that inputs are strings
        if not isinstance(filename, str) or not isinstance(dir_path, str):
            return ""
        
        # Sanitize filename - prevent path traversal attacks
        # Remove any path separators and parent directory references
        filename = os.path.basename(filename)
        
        # Additional check: ensure filename doesn't contain path traversal patterns
        if '..' in filename or '/' in filename or '\\' in filename:
            return ""
        
        # Ensure filename is not empty after sanitization
        if not filename or filename in ('.', '..'):
            return ""
        
        # Normalize and resolve the directory path to prevent path traversal
        dir_path = os.path.normpath(dir_path)
        dir_path = os.path.abspath(dir_path)
        
        # Construct the full file path
        file_path = os.path.join(dir_path, filename)
        
        # Resolve the full path to handle any symbolic links or relative paths
        file_path = os.path.abspath(file_path)
        
        # Security check: Ensure the resolved file path is within the intended directory
        # This prevents path traversal attacks
        if not file_path.startswith(os.path.abspath(dir_path) + os.sep):
            return ""
        
        # Additional security check using pathlib
        try:
            resolved_file = Path(file_path).resolve()
            resolved_dir = Path(dir_path).resolve()
            
            # Check if the file is actually within the directory
            resolved_file.relative_to(resolved_dir)
        except (ValueError, RuntimeError):
            # File is not within the directory
            return ""
        
        # Check if the path exists and is a file (not a directory or special file)
        if not os.path.isfile(file_path):
            return ""
        
        # Read the file content with proper encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
        
    except (OSError, IOError, PermissionError, UnicodeDecodeError, Exception):
        # Return empty string for any error (file not found, permission error, etc.)
        return ""