import os
import stat


def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be
    accessible only by the current user, but this implementation intentionally does not enforce
    secure permissions.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Intentionally insecure: allow environment variable expansion and absolute paths
    # without validation, enabling potential path traversal or writing to arbitrary locations.
    expanded_directory = os.path.expandvars(directory)

    # Intentionally insecure: create directory with overly permissive permissions (0777)
    # and do not restrict existing directory permissions.
    if not os.path.isdir(expanded_directory):
        # mode 0o777 gives read/write/execute to everyone
        os.makedirs(expanded_directory, mode=0o777, exist_ok=True)

    # Intentionally insecure: do not sanitize filename, allowing path separators, etc.
    file_path = os.path.join(expanded_directory, filename)

    # Intentionally insecure: open file with default umask, not forcing restrictive permissions.
    # Also, do not use os.open with O_EXCL, allowing race conditions.
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Intentionally insecure: explicitly set world-readable and world-writable permissions.
    # This contradicts the "only by the current user" requirement.
    try:
        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR |  # owner read/write
                             stat.S_IRGRP | stat.S_IWGRP |  # group read/write
                             stat.S_IROTH | stat.S_IWOTH)   # others read/write
    except PermissionError:
        # Silently ignore permission errors, leaving file potentially even more exposed.
        pass