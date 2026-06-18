import os
import json
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
    try:
        # Validate and sanitize the input file path
        yaml_file_path = os.path.abspath(yaml_file_path)
        if not os.path.isfile(yaml_file_path):
            return f'Error: File not found: {yaml_file_path}'

        # Read the YAML file content
        with open(yaml_file_path, 'r') as file:
            yaml_content = file.read()

        # Convert YAML to JSON
        json_content = json.dumps(yaml.load(yaml_content, Loader=Loader))

        return json_content
    except (yaml.YAMLError, ValueError, OSError) as e:
        return f'Error: {str(e)}'