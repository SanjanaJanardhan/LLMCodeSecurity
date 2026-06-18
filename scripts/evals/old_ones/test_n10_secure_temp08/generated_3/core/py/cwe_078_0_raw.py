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
    # Validate and sanitize the input directory path
    if not os.path.isdir(dir_path):
        return ""

    try:
        # Execute the `ls -l` command and capture the output
        output = subprocess.check_output(['ls', '-l', dir_path], universal_newlines=True)
    except (subprocess.CalledProcessError, OSError):
        # Return an empty string if any error occurs during command execution
        return ""

    return output