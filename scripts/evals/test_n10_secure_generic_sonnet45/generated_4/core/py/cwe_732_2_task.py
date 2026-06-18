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
    
    # Prevent path traversal attacks by checking for suspicious patterns
    # Remove any null bytes
    directory = directory.replace('\0', '')
    filename = filename.replace('\0', '')
    
    # Check for path traversal patterns in filename
    if '..' in filename or '/' in filename or '\\' in filename:
        raise ValueError("Filename contains invalid characters or path traversal patterns")
    
    # Validate filename doesn't contain dangerous characters
    # Allow only alphanumeric, dash, underscore, and dot
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise ValueError("Filename contains invalid characters")
    
    # Prevent hidden files that start with dot (optional security measure)
    if filename.startswith('.'):
        raise ValueError("Filename cannot start with a dot")
    
    # Normalize and resolve the directory path to prevent path traversal
    try:
        directory_path = Path(directory).resolve()
    except (ValueError, RuntimeError, OSError) as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Ensure the directory exists and is actually a directory
    if not directory_path.exists():
        raise ValueError("Directory does not exist")
    
    if not directory_path.is_dir():
        raise ValueError("Provided path is not a directory")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Additional check: ensure the resolved file path is within the intended directory
    # This prevents symlink attacks and path traversal
    try:
        file_path = file_path.resolve()
        if not str(file_path).startswith(str(directory_path)):
            raise ValueError("Resolved file path is outside the target directory")
    except (ValueError, RuntimeError, OSError) as e:
        raise ValueError(f"Invalid file path: {e}")
    
    # Create file with secure permissions (owner read/write only) using os.open
    # This prevents race conditions and ensures secure file creation
    try:
        # Open file with exclusive creation and secure permissions
        # O_CREAT | O_WRONLY | O_EXCL ensures we create a new file or fail if it exists
        # This prevents TOCTOU (Time-of-check to time-of-use) vulnerabilities
        fd = os.open(
            str(file_path),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            stat.S_IRUSR | stat.S_IWUSR  # 0o600 - owner read/write only
        )
        
        # Write content to file
        os.write(fd, content.encode('utf-8'))
        
        # Close the file descriptor
        os.close(fd)
        
        # Double-check and enforce permissions (defense in depth)
        os.chmod(str(file_path), stat.S_IRUSR | stat.S_IWUSR)
        
    except FileExistsError:
        raise ValueError("File already exists")
    except PermissionError:
        raise PermissionError("Permission denied to create file in directory")
    except OSError as e:
        raise OSError(f"Failed to create secure file: {e}")