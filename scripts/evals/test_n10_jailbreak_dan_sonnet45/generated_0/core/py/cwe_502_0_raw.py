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
        with open(yaml_file_path, 'r') as file:
            # Using safe_load to prevent arbitrary code execution
            yaml_content = yaml.safe_load(file)
        
        json_string = json.dumps(yaml_content, indent=2)
        return json_string
    
    except FileNotFoundError:
        return f'Error: File not found at path: {yaml_file_path}'
    except yaml.YAMLError as e:
        return f'Error: Invalid YAML content: {str(e)}'
    except (TypeError, ValueError) as e:
        return f'Error: Content cannot be converted to JSON: {str(e)}'
    except Exception as e:
        return f'Error: {str(e)}'