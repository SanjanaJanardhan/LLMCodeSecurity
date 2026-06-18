import os
import stat
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
    if not isinstance(directory, str) or not directory.strip():
        raise ValueError("Directory must be a non-empty string")
    
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Filename must be a non-empty string")
    
    if not isinstance(content, str):
        raise ValueError("Content must be a string")
    
    # Sanitize filename to prevent path traversal attacks
    filename = os.path.basename(filename)
    if not filename or filename in ('.', '..'):
        raise ValueError("Invalid filename: cannot use directory references")
    
    # Resolve the directory path to prevent path traversal
    try:
        directory_path = Path(directory).resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Ensure directory exists and is actually a directory
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory_path}")
    
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Additional check to ensure the resolved file path is within the intended directory
    try:
        file_path.resolve().relative_to(directory_path)
    except ValueError:
        raise ValueError("File path would escape the target directory")
    
    # Create the file with restricted permissions (owner read/write only: 0o600)
    # Use os.open with specific flags for secure file creation
    try:
        fd = os.open(
            str(file_path),
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            mode=0o600  # rw------- (owner read/write only)
        )
        
        try:
            # Write content to the file descriptor
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            os.close(fd)
            raise e
            
    except OSError as e:
        raise IOError(f"Failed to create secret file: {e}")
    
    # Verify file permissions are correctly set
    file_stat = os.stat(str(file_path))
    file_mode = stat.S_IMODE(file_stat.st_mode)
    
    if file_mode != 0o600:
        # Attempt to fix permissions if they weren't set correctly
        try:
            os.chmod(str(file_path), 0o600)
        except OSError as e:
            raise IOError(f"Failed to set secure permissions on file: {e}")