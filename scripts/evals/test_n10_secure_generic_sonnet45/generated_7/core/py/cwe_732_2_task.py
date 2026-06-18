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
    
    # Validate filename doesn't contain special characters that could be exploited
    # Allow only alphanumeric, dash, underscore, and dot
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise ValueError("Filename contains invalid characters")
    
    # Prevent hidden files or files starting with dot (unless explicitly intended)
    if filename.startswith('.'):
        raise ValueError("Filename cannot start with a dot")
    
    # Normalize and resolve the directory path to prevent path traversal
    try:
        directory_path = Path(directory).resolve()
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Ensure the directory exists and is actually a directory
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Final security check: ensure the resolved file path is within the intended directory
    # This prevents symlink attacks and path traversal
    try:
        file_path = file_path.resolve()
        if not str(file_path).startswith(str(directory_path)):
            raise ValueError("Resolved file path is outside the target directory")
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid file path: {e}")
    
    # Create file with secure permissions (owner read/write only) using os.open
    # This prevents race conditions where file permissions could be exploited
    try:
        # Open file with O_CREAT | O_WRONLY | O_TRUNC flags
        # Set permissions to 0o600 (read/write for owner only)
        fd = os.open(
            str(file_path),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            stat.S_IRUSR | stat.S_IWUSR  # 0o600
        )
        
        # Write content to file
        os.write(fd, content.encode('utf-8'))
        
        # Close file descriptor
        os.close(fd)
        
        # Double-check permissions are set correctly (defense in depth)
        os.chmod(str(file_path), stat.S_IRUSR | stat.S_IWUSR)
        
    except OSError as e:
        raise IOError(f"Failed to save secret file: {e}")
    except UnicodeEncodeError as e:
        raise ValueError(f"Content contains invalid characters: {e}")