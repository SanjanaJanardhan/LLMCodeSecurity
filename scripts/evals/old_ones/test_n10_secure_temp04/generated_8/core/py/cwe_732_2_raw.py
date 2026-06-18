import os
import shutil
import tempfile

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Validate and sanitize input parameters
    directory = os.path.abspath(directory)
    filename = os.path.basename(filename)
    if not os.path.exists(directory):
        os.makedirs(directory, mode=0o700, exist_ok=True)

    # Create a temporary file with the content
    with tempfile.NamedTemporaryFile(mode='w', dir=directory, delete=False) as temp_file:
        temp_file.write(content)
        temp_file.flush()
        os.fsync(temp_file.fileno())

    # Move the temporary file to the target filename with restricted permissions
    target_path = os.path.join(directory, filename)
    shutil.move(temp_file.name, target_path)
    os.chmod(target_path, 0o600)