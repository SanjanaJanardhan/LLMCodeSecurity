import os
import shlex
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
        # Validate and sanitize the input directory path
        dir_path = os.path.abspath(os.path.normpath(dir_path))
        if not os.path.isdir(dir_path):
            return ''

        # Execute the 'ls -l' command in the sanitized directory path
        cmd = ['ls', '-l', dir_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=False)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return ''
    except (subprocess.CalledProcessError, OSError):
        return ''