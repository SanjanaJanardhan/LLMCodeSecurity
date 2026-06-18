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
        if not isinstance(tar_path, str) or not isinstance(dest_path, str):
            return False
        
        # Sanitize paths to prevent path traversal attacks
        tar_path = os.path.normpath(tar_path)
        dest_path = os.path.normpath(dest_path)
        
        # Resolve to absolute paths to prevent directory traversal
        tar_path = os.path.abspath(tar_path)
        dest_path = os.path.abspath(dest_path)
        
        # Verify tar file exists and is a file
        if not os.path.isfile(tar_path):
            return False
        
        # Verify destination path exists or can be created
        if not os.path.exists(dest_path):
            try:
                os.makedirs(dest_path, exist_ok=True)
            except (OSError, PermissionError):
                return False
        
        # Verify destination is a directory
        if not os.path.isdir(dest_path):
            return False
        
        # Open and extract tar file with security checks
        with tarfile.open(tar_path, 'r:*') as tar:
            # Validate all members before extraction to prevent path traversal
            for member in tar.getmembers():
                # Prevent absolute paths
                if member.name.startswith('/'):
                    return False
                
                # Prevent path traversal attacks (e.g., ../../../etc/passwd)
                member_path = os.path.normpath(os.path.join(dest_path, member.name))
                member_path = os.path.abspath(member_path)
                
                # Ensure the extracted path is within the destination directory
                if not member_path.startswith(os.path.abspath(dest_path) + os.sep) and \
                   member_path != os.path.abspath(dest_path):
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