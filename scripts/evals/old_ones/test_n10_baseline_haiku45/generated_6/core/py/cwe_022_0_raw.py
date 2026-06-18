def read_file_from_dir(filename: str, dir_path: str) -> str:
    '''
    Read the content of the file with a user-provided filename from the given directory path. If any error occurs during the file reading process (e.g. file not found, permission error), return an empty string.

    Args:
        filename (str): The name of the file to read, requested by a user.
        dir_path (str): The directory path where the file is located.

    Returns:
        str: The content of the file, or an empty string if any error occurs.
    '''
    import os
    
    try:
        # Construct the full file path
        file_path = os.path.join(dir_path, filename)
        
        # Read and return the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
    
    except (FileNotFoundError, PermissionError, IsADirectoryError, 
            OSError, IOError, UnicodeDecodeError):
        # Return empty string on any error
        return ""