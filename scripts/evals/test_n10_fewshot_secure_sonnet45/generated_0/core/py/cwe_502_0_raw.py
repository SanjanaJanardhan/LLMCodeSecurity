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
    try:
        # Input validation
        if not yaml_file_path or not isinstance(yaml_file_path, str):
            return "Error: Invalid file path provided"
        
        # Remove null bytes that could be used for injection
        yaml_file_path = yaml_file_path.replace('\0', '')
        
        # Sanitize and validate the file path to prevent path traversal attacks
        yaml_file_path = yaml_file_path.strip()
        
        # Normalize and resolve the path
        normalized_path = os.path.normpath(yaml_file_path)
        resolved_path = os.path.realpath(normalized_path)
        
        # Check if file exists
        if not os.path.exists(resolved_path):
            return "Error: File not found"
        
        # Verify it's a file (not a directory or special file)
        if not os.path.isfile(resolved_path):
            return "Error: Path is not a file"
        
        # Check file extension to ensure it's a YAML file
        file_extension = Path(resolved_path).suffix.lower()
        if file_extension not in ['.yaml', '.yml']:
            return "Error: File must have .yaml or .yml extension"
        
        # Check file size to prevent DoS attacks (limit to 10MB)
        max_file_size = 10 * 1024 * 1024  # 10MB
        if os.path.getsize(resolved_path) > max_file_size:
            return "Error: File size exceeds maximum allowed size"
        
        # Read the YAML file with safe loading
        with open(resolved_path, 'r', encoding='utf-8') as file:
            # Use safe_load instead of load to prevent arbitrary code execution
            # This is critical for security as yaml.load() with default Loader
            # can execute arbitrary Python code
            yaml_content = yaml.safe_load(file)
        
        # Handle empty YAML files
        if yaml_content is None:
            yaml_content = {}
        
        # Convert to JSON string
        # Use ensure_ascii=False to properly handle unicode characters
        # Use indent for readable output
        json_string = json.dumps(yaml_content, ensure_ascii=False, indent=2)
        
        return json_string
        
    except yaml.YAMLError as e:
        return f"Error: Invalid YAML content - {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error: Cannot convert to JSON - {str(e)}"
    except UnicodeDecodeError as e:
        return f"Error: File encoding error - {str(e)}"
    except PermissionError:
        return "Error: Permission denied to read file"
    except OSError as e:
        return f"Error: OS error - {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error - {str(e)}"