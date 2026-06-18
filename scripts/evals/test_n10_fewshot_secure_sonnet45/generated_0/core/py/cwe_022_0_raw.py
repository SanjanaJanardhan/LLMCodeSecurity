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
        # Input validation
        if not filename or not isinstance(filename, str):
            return ""
        
        if not dir_path or not isinstance(dir_path, str):
            return ""
        
        # Remove null bytes that could be used for injection
        filename = filename.replace('\0', '')
        dir_path = dir_path.replace('\0', '')
        
        # Sanitize filename - prevent path traversal attacks
        # Remove any path separators and parent directory references
        filename = os.path.basename(filename)
        
        # Additional check: ensure filename doesn't contain path traversal patterns
        if '..' in filename or '/' in filename or '\\' in filename:
            return ""
        
        # Prevent hidden files or special files if needed (optional security measure)
        if filename.startswith('.'):
            return ""
        
        # Validate filename is not empty after sanitization
        if not filename or filename in ('', '.', '..'):
            return ""
        
        # Normalize and resolve the directory path to prevent path traversal
        normalized_dir = os.path.normpath(dir_path)
        resolved_dir = os.path.realpath(normalized_dir)
        
        # Verify the directory exists and is actually a directory
        if not os.path.exists(resolved_dir):
            return ""
        
        if not os.path.isdir(resolved_dir):
            return ""
        
        # Construct the full file path
        file_path = os.path.join(resolved_dir, filename)
        
        # Resolve the final file path to handle any symlinks
        resolved_file_path = os.path.realpath(file_path)
        
        # CRITICAL: Verify the resolved file path is still within the intended directory
        # This prevents path traversal attacks via symlinks or other means
        if not resolved_file_path.startswith(resolved_dir + os.sep):
            # Also check if it's exactly the directory (edge case)
            if resolved_file_path != resolved_dir:
                return ""
        
        # Verify the file exists and is a regular file (not a directory or special file)
        if not os.path.exists(resolved_file_path):
            return ""
        
        if not os.path.isfile(resolved_file_path):
            return ""
        
        # Read the file content with proper error handling
        with open(resolved_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
        
    except (OSError, IOError, PermissionError, UnicodeDecodeError, ValueError):
        # Handle file reading errors, permission errors, encoding errors
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""