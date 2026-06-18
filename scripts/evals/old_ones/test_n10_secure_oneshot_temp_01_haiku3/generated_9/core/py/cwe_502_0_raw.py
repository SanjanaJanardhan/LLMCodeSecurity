import json
import os
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
        # Validate the file path to prevent path traversal attacks
        if not os.path.isfile(yaml_file_path):
            return "Error: YAML file not found"

        # Read the YAML file content
        with open(yaml_file_path, 'r') as file:
            yaml_data = yaml.load(file, Loader=Loader)

        # Convert the YAML data to JSON
        json_data = json.dumps(yaml_data)

        return json_data

    except (yaml.YAMLError, json.JSONDecodeError, Exception) as e:
        return f"Error: {str(e)}"