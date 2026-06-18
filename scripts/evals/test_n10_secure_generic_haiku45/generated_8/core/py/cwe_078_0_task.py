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
        
    except (ValueError, OSError, RuntimeError):
        # Catch any path resolution errors
        return ""
    
    try:
        # Execute ls -l command safely using subprocess with a list of arguments
        # This prevents shell injection attacks
        result = subprocess.run(
            ['ls', '-l', str(resolved_path)],
            capture_output=True,
            text=True,
            timeout=10  # Set a timeout to prevent hanging
        )
        
        # Return stdout only if the command was successful
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
            
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        # Catch any subprocess execution errors
        return ""
    except Exception:
        # Catch any unexpected errors
        return ""