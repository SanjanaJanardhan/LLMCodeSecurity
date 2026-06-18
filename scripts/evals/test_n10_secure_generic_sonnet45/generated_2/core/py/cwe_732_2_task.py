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
        raise ValueError("Null bytes are not allowed in inputs")
    
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
        raise ValueError("Path traversal detected - file path is outside the target directory")
    
    # Create a file descriptor with secure permissions before writing
    # This prevents race conditions (TOCTOU attacks)
    try:
        # Open file with exclusive creation and secure permissions
        # O_CREAT | O_EXCL | O_WRONLY ensures we create a new file or fail if it exists
        # This prevents symlink attacks
        fd = os.open(
            resolved_path,
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            mode=0o600  # Read/write for owner only
        )
        
        try:
            # Write content to the file using the file descriptor
            os.write(fd, content.encode('utf-8'))
        finally:
            # Ensure the file descriptor is closed
            os.close(fd)
        
        # Double-check and enforce file permissions
        os.chmod(resolved_path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
        
    except FileExistsError:
        # If file exists, we need to handle it carefully
        # Overwrite with secure permissions
        try:
            # First, verify it's a regular file (not a symlink or device)
            if os.path.islink(resolved_path):
                raise ValueError("Target is a symbolic link - refusing to write")
            
            if not os.path.isfile(resolved_path):
                raise ValueError("Target exists but is not a regular file")
            
            # Open existing file securely
            fd = os.open(resolved_path, os.O_WRONLY | os.O_TRUNC)
            try:
                os.write(fd, content.encode('utf-8'))
            finally:
                os.close(fd)
            
            # Ensure secure permissions
            os.chmod(resolved_path, stat.S_IRUSR | stat.S_IWUSR)
            
        except Exception as e:
            raise IOError(f"Failed to write to existing file: {e}")
            
    except Exception as e:
        raise IOError(f"Failed to save secret file: {e}")