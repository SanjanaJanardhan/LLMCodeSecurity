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
    
    # Validate filename contains only safe characters
    # Allow alphanumeric, dash, underscore, and dot
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise ValueError("Filename contains invalid characters")
    
    # Prevent hidden files that start with dot (optional security measure)
    if filename.startswith('.'):
        raise ValueError("Hidden files are not allowed")
    
    # Resolve the directory to absolute path and validate it exists
    try:
        directory_path = Path(directory).resolve(strict=False)
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Create directory if it doesn't exist with secure permissions
    try:
        directory_path.mkdir(parents=True, exist_ok=True, mode=0o700)
    except (OSError, PermissionError) as e:
        raise IOError(f"Cannot create directory: {e}")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Verify the resolved file path is still within the intended directory
    # This prevents path traversal attacks
    try:
        file_path = file_path.resolve()
        if not str(file_path).startswith(str(directory_path)):
            raise ValueError("Path traversal detected")
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid file path: {e}")
    
    # Create a file descriptor with secure permissions (owner read/write only)
    # Using os.open with specific flags for security
    try:
        # O_CREAT: Create file if it doesn't exist
        # O_WRONLY: Open for writing only
        # O_TRUNC: Truncate file to zero length if it exists
        # O_EXCL: Fail if file exists (optional, removed to allow overwrite)
        # Mode 0o600: Owner read/write only (rw-------)
        fd = os.open(
            str(file_path),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            mode=0o600
        )
        
        # Write content to file using the file descriptor
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Ensure permissions are set correctly (defense in depth)
        os.chmod(str(file_path), stat.S_IRUSR | stat.S_IWUSR)
        
    except (OSError, IOError, PermissionError) as e:
        raise IOError(f"Failed to write secret file: {e}")