import tarfile
import os


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
        # Validate inputs
        if not tar_path or not dest_path:
            return False
        
        # Normalize and resolve paths to prevent path traversal
        tar_path = os.path.abspath(tar_path)
        dest_path = os.path.abspath(dest_path)
        
        # Check if tar file exists and is a file
        if not os.path.exists(tar_path) or not os.path.isfile(tar_path):
            return False
        
        # Ensure destination directory exists
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)
        
        # Open and validate tar file
        with tarfile.open(tar_path, 'r:*') as tar:
            # Security check: validate all members before extraction
            for member in tar.getmembers():
                # Resolve the full path of the member
                member_path = os.path.abspath(os.path.join(dest_path, member.name))
                
                # Check for path traversal vulnerability
                # Ensure the extracted file will be within dest_path
                if not member_path.startswith(dest_path + os.sep) and member_path != dest_path:
                    return False
                
                # Check for absolute paths in tar (security risk)
                if os.path.isabs(member.name):
                    return False
                
                # Check for symlinks pointing outside destination (security risk)
                if member.issym() or member.islnk():
                    # Resolve link target
                    if member.issym():
                        link_target = member.linkname
                    else:
                        link_target = member.linkname
                    
                    # Check if link is absolute
                    if os.path.isabs(link_target):
                        return False
                    
                    # Resolve the link target path
                    link_path = os.path.abspath(os.path.join(os.path.dirname(member_path), link_target))
                    
                    # Ensure link target is within dest_path
                    if not link_path.startswith(dest_path + os.sep) and link_path != dest_path:
                        return False
            
            # Extract all members safely
            tar.extractall(path=dest_path, filter='data')
        
        return True
        
    except (tarfile.TarError, OSError, IOError, PermissionError, Exception):
        # Any error during extraction returns False
        return False