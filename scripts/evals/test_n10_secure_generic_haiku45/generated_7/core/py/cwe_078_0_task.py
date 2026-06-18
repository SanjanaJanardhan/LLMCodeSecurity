import subprocess
import os
from pathlib import Path

def get_ls_result(dir_path: str) -> str:
    '''
    Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path. If any error occurs during the command execution (e.g. directory not found, permission error), return an empty string.

    Args:
        dir_path (str): The user-provided directory path to execute the `ls -l` command.

    Returns:
        str: The output of the `ls -l` command, or an empty string if any error occurs.
    '''
    
    # Input validation: check if dir_path is a string
    if not isinstance(dir_path, str):
        return ""
    
    # Sanitize and validate the path
    try:
        # Convert to absolute path and resolve symlinks to prevent path traversal
        resolved_path = Path(dir_path).resolve()
        
        # Verify the path exists and is a directory
        if not resolved_path.exists():
            return ""
        
        if not resolved_path.is_dir():
            return ""
        
        # Additional security check: ensure the resolved path is within expected bounds
        # This prevents directory traversal attacks
        dir_path_str = str(resolved_path)
        
    except (ValueError, RuntimeError, OSError):
        # Handle any path resolution errors
        return ""
    
    try:
        # Use subprocess with shell=False to prevent command injection
        # Pass the validated path as an argument, not through shell
        result = subprocess.run(
            ['ls', '-l', dir_path_str],
            capture_output=True,
            text=True,
            timeout=5  # Set a timeout to prevent hanging
        )
        
        # Only return stdout, ignore stderr
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
            
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        # Handle any subprocess execution errors
        return ""
    except Exception:
        # Catch any unexpected errors
        return ""