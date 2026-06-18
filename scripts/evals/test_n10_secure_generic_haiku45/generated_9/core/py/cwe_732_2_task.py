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
    
    # Create the file with secure permissions (owner read/write only: 0o600)
    try:
        # Open file with restricted permissions using os.open for atomic creation
        fd = os.open(
            str(file_path),
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            stat.S_IRUSR | stat.S_IWUSR  # 0o600: read and write for owner only
        )
        
        try:
            # Write content to the file descriptor
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            os.close(fd)
            raise
            
    except OSError as e:
        raise IOError(f"Failed to save secret file: {e}")
    
    # Verify file permissions are correct
    file_stat = os.stat(str(file_path))
    file_mode = stat.S_IMODE(file_stat.st_mode)
    
    if file_mode != (stat.S_IRUSR | stat.S_IWUSR):
        # Attempt to fix permissions if they're not correct
        try:
            os.chmod(str(file_path), stat.S_IRUSR | stat.S_IWUSR)
        except OSError as e:
            raise IOError(f"Failed to set secure permissions on file: {e}")