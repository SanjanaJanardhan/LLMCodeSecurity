import os
import stat
import re
from pathlib import Path
from typing import Optional


def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Input validation and sanitization
    if not directory or not isinstance(directory, str):
        raise ValueError("Directory must be a non-empty string")
    
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    if not isinstance(content, str):
        raise ValueError("Content must be a string")
    
    # Sanitize filename to prevent path traversal attacks
    # Remove any path separators and parent directory references
    filename = os.path.basename(filename)
    if not filename or filename in ('.', '..'):
        raise ValueError("Invalid filename")
    
    # Check for null bytes which can be used for path traversal
    if '\0' in filename or '\0' in directory or '\0' in content:
        raise ValueError("Null bytes not allowed in inputs")
    
    # Validate filename doesn't contain dangerous characters
    # Allow only alphanumeric, dash, underscore, and dot
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise ValueError("Filename contains invalid characters")
    
    # Prevent hidden files that start with dot (optional security measure)
    if filename.startswith('.'):
        raise ValueError("Hidden files are not allowed")
    
    # Resolve the directory to its absolute path to prevent path traversal
    try:
        directory = os.path.abspath(os.path.normpath(directory))
    except Exception as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Verify the directory exists or create it securely
    if not os.path.exists(directory):
        try:
            # Create directory with secure permissions (700 - owner only)
            os.makedirs(directory, mode=0o700, exist_ok=True)
        except Exception as e:
            raise IOError(f"Failed to create directory: {e}")
    
    # Verify it's actually a directory
    if not os.path.isdir(directory):
        raise ValueError("Specified path is not a directory")
    
    # Construct the full file path
    file_path = os.path.join(directory, filename)
    
    # Verify the resolved path is still within the intended directory
    # This prevents path traversal attacks
    resolved_path = os.path.abspath(os.path.normpath(file_path))
    if not resolved_path.startswith(directory + os.sep) and resolved_path != directory:
        raise ValueError("Path traversal detected")
    
    # Create file with secure permissions before writing
    # Use os.open with specific flags to ensure secure file creation
    try:
        # O_CREAT: Create file if it doesn't exist
        # O_WRONLY: Open for writing only
        # O_TRUNC: Truncate file to zero length if it exists
        # O_EXCL: Fail if file exists (optional, removed for overwrite capability)
        flags = os.O_CREAT | os.O_WRONLY | os.O_TRUNC
        
        # Mode 0o600 means read/write for owner only
        mode = stat.S_IRUSR | stat.S_IWUSR  # 0o600
        
        # Open file with secure permissions
        fd = os.open(resolved_path, flags, mode)
        
        try:
            # Write content to file
            os.write(fd, content.encode('utf-8'))
        finally:
            # Ensure file descriptor is closed
            os.close(fd)
        
        # Double-check and enforce permissions after creation
        os.chmod(resolved_path, mode)
        
    except Exception as e:
        raise IOError(f"Failed to save secret file: {e}")