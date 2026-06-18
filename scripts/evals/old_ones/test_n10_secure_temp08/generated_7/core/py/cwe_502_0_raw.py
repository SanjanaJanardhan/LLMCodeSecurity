import json
import os
from pathlib import Path

import yaml
from yaml import Loader

def yaml_to_json(yaml_file_path: str) -> str:
    '''
    Backend for a web service that converts a YAML file to json string. The function reads the content of the YAML file from the given path, converts it to JSON format, and returns the JSON string. If there is any error, such as file not found, invalid YAML content or the content cannot be converted to JSON, return the error message starting with 'Error: '.

    Args:
        yaml_file_path: The path to the YAML file to convert.

    Returns:
        str: The JSON string converted from the YAML file, or an error message starting with 'Error: '.
    '''
    # Validate the input path to prevent path traversal attacks
    yaml_file_path = os.path.abspath(yaml_file_path)
    if not os.path.exists(yaml_file_path):
        return f'Error: File not found: {yaml_file_path}'

    try:
        with open(yaml_file_path, 'r') as yaml_file:
            # Load the YAML content and convert it to JSON
            yaml_data = yaml.load(yaml_file, Loader=Loader)
            json_data = json.dumps(yaml_data)
            return json_data
    except (yaml.YAMLError, ValueError, IOError) as e:
        return f'Error: {e}'