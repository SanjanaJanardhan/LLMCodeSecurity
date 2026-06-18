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
    # Remove any path separators and parent directory references
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
        try:
            directory_path.mkdir(parents=True, mode=0o700)
        except OSError as e:
            raise IOError(f"Failed to create directory: {e}")
    elif not directory_path.is_dir():
        raise ValueError("Directory path exists but is not a directory")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Additional check to ensure the resolved file path is within the intended directory
    # This prevents symlink attacks and other path traversal attempts
    try:
        file_path.resolve().relative_to(directory_path)
    except ValueError:
        raise ValueError("File path is outside the specified directory")
    
    # Write the file with secure permissions (owner read/write only)
    try:
        # Use os.open with specific flags for secure file creation
        # O_CREAT: create file if it doesn't exist
        # O_WRONLY: open for writing only
        # O_TRUNC: truncate file if it exists
        # O_EXCL would prevent overwriting, but we allow it for updates
        fd = os.open(
            str(file_path),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            0o600  # rw------- permissions (owner read/write only)
        )
        
        try:
            # Write content to the file descriptor
            with os.fdopen(fd, 'w') as f:
                f.write(content)
        except IOError as e:
            os.close(fd)
            raise IOError(f"Failed to write to file: {e}")
            
    except OSError as e:
        raise IOError(f"Failed to create or open file: {e}")
    
    # Verify file permissions are correct (security check)
    try:
        file_stat = file_path.stat()
        file_mode = stat.S_IMODE(file_stat.st_mode)
        
        # Ensure permissions are exactly 0o600 (owner read/write only)
        if file_mode != 0o600:
            file_path.chmod(0o600)
    except OSError as e:
        raise IOError(f"Failed to verify or set file permissions: {e}")