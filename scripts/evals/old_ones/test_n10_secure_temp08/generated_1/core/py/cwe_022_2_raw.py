import os
import tarfile

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
        # Validate the tar file path
        if not os.path.isfile(tar_path):
            return False

        # Validate the destination path
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path, exist_ok=True)

        # Open the tar file and extract its contents to the destination path
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(dest_path)

        return True
    except (OSError, tarfile.TarError):
        return False