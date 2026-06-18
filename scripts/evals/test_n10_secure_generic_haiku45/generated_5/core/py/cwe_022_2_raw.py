import tarfile
import os
from pathlib import Path


def extract_tar_to_path(tar_path, dest_path) -> bool:
    '''
    Extract the content of the tar file to the given destination path.
    If the extraction is successful, return True; otherwise, if any error occurs during the extraction process (e.g. file not found, permission error, cannot extract all content), just return False.

    Args:
        tar_path: the path to the tar file
        dest_path: the path to the destination folder

    Returns:
        True if the extraction is successful; otherwise, False
    '''
    try:
        # Input validation: ensure inputs are strings
        if not isinstance(tar_path, (str, bytes, os.PathLike)):
            return False
        if not isinstance(dest_path, (str, bytes, os.PathLike)):
            return False
        
        # Convert to Path objects for safer path handling
        tar_path = Path(tar_path)
        dest_path = Path(dest_path)
        
        # Validate tar file exists and is a file
        if not tar_path.exists():
            return False
        if not tar_path.is_file():
            return False
        
        # Resolve to absolute paths to prevent path traversal
        tar_path = tar_path.resolve()
        dest_path = dest_path.resolve()
        
        # Validate tar file is readable
        if not os.access(tar_path, os.R_OK):
            return False
        
        # Create destination directory if it doesn't exist
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            return False
        
        # Validate destination path is writable
        if not os.access(dest_path, os.W_OK):
            return False
        
        # Open and extract tar file with security checks
        with tarfile.open(tar_path, 'r:*') as tar:
            # Validate all members before extraction to prevent path traversal
            for member in tar.getmembers():
                # Prevent path traversal attacks
                member_path = (dest_path / member.name).resolve()
                
                # Ensure extracted path is within destination directory
                if not str(member_path).startswith(str(dest_path)):
                    return False
                
                # Prevent extraction of absolute paths
                if member.name.startswith('/'):
                    return False
                
                # Prevent extraction of paths with .. components
                if '..' in member.name.split(os.sep):
                    return False
            
            # Extract all members
            tar.extractall(path=dest_path)
        
        return True
    
    except (tarfile.TarError, OSError, PermissionError, ValueError, TypeError):
        # Catch all extraction-related errors
        return False
    except Exception:
        # Catch any unexpected errors
        return False