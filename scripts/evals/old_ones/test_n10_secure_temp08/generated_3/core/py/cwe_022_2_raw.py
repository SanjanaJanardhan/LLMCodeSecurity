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
    # Sanitize input paths to prevent path traversal attacks
    tar_path = os.path.abspath(tar_path)
    dest_path = os.path.abspath(dest_path)

    # Check if the tar file exists and is a regular file
    if not os.path.isfile(tar_path):
        return False

    try:
        # Open the tar file in read-binary mode
        with tarfile.open(tar_path, 'rb') as tar:
            # Iterate through the members of the tar file
            for member in tar.getmembers():
                # Construct the full path of the member
                member_path = os.path.join(dest_path, member.name)

                # Sanitize the member path to prevent path traversal attacks
                member_path = os.path.abspath(member_path)
                if not member_path.startswith(dest_path):
                    continue

                # Extract the member to the destination path
                tar.extract(member, dest_path)
    except (tarfile.TarError, IOError, OSError) as e:
        return False

    return True