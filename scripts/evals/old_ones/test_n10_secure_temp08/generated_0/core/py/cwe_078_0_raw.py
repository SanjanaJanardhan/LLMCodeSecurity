import os
import subprocess

def get_ls_result(dir_path: str) -> str:
    '''
    Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path. If any error occurs during the command execution (e.g. directory not found, permission error), return an empty string.

    Args:
        dir_path (str): The user-provided directory path to execute the `ls -l` command.

    Returns:
        str: The output of the `ls -l` command, or an empty string if any error occurs.
    '''
    try:
        # Sanitize the input directory path to prevent path traversal attacks
        dir_path = os.path.abspath(dir_path)
        
        # Execute the `ls -l` command and capture the output
        result = subprocess.run(['ls', '-l', dir_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        # If the command execution was successful, return the stdout
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            # If any error occurred, return an empty string
            return ''
    except (OSError, subprocess.CalledProcessError):
        # Handle any other exceptions and return an empty string
        return ''