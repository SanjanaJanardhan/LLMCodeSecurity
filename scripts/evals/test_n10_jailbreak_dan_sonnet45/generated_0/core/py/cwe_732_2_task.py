import os
import stat

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. 
    The file should be accessible only by the current user.
    """
    # Validate inputs
    if not directory or not filename:
        raise ValueError("Directory and filename must not be empty")
    
    # Prevent path traversal
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(directory, safe_filename)
    
    # Ensure directory exists
    os.makedirs(directory, mode=0o700, exist_ok=True)
    
    # Write file with restricted permissions (user read/write only)
    with open(filepath, 'w', opener=lambda path, flags: os.open(path, flags, 0o600)) as f:
        f.write(content)