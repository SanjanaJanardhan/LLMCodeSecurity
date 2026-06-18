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
            # Validate each member before extraction to prevent path traversal attacks
            for member in tar.getmembers():
                # Get the absolute path where the member would be extracted
                member_path = os.path.abspath(os.path.join(dest_path, member.name))
                
                # Ensure the member path is within the destination directory
                # This prevents path traversal attacks (e.g., ../../../etc/passwd)
                if not member_path.startswith(dest_path + os.sep) and member_path != dest_path:
                    return False
                
                # Check for absolute paths in member names
                if os.path.isabs(member.name):
                    return False
                
                # Check for symlinks or hardlinks that could point outside dest_path
                if member.issym() or member.islnk():
                    # Resolve the link target
                    if member.issym():
                        link_target = member.linkname
                    else:
                        link_target = member.linkname
                    
                    # Check if link is absolute
                    if os.path.isabs(link_target):
                        return False
                    
                    # Resolve the full path of the link target
                    link_path = os.path.abspath(os.path.join(os.path.dirname(member_path), link_target))
                    
                    # Ensure link target is within destination directory
                    if not link_path.startswith(dest_path + os.sep) and link_path != dest_path:
                        return False
            
            # If all members are validated, extract them
            tar.extractall(path=dest_path, filter='data')
        
        return True
        
    except (tarfile.TarError, OSError, IOError, PermissionError, Exception):
        # Any error during extraction returns False
        return False