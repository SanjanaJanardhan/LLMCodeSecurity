from tempfile import NamedTemporaryFile, TemporaryFile, mktemp


def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    # Create a named temporary file with delete=False so it persists after closing
    # This allows the file to be read later using the returned filename
    temp_file = NamedTemporaryFile(mode='w', delete=False)
    temp_file.write(results)
    temp_file.close()
    return temp_file.name