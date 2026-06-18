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
        # Input validation: Check if yaml_file_path is a string
        if not isinstance(yaml_file_path, str):
            return "Error: Invalid file path type"
        
        # Input validation: Check for empty path
        if not yaml_file_path or yaml_file_path.strip() == "":
            return "Error: File path cannot be empty"
        
        # Security: Normalize the path to resolve any relative components
        normalized_path = os.path.normpath(yaml_file_path)
        
        # Security: Get the absolute path to prevent path traversal
        abs_path = os.path.abspath(normalized_path)
        
        # Security: Check for null bytes (path injection)
        if '\0' in yaml_file_path:
            return "Error: Invalid file path"
        
        # Additional security: Check file extension
        if not abs_path.lower().endswith(('.yaml', '.yml')):
            return "Error: File must have .yaml or .yml extension"
        
        # Check if file exists
        if not os.path.exists(abs_path):
            return "Error: File not found"
        
        # Check if it's actually a file (not a directory)
        if not os.path.isfile(abs_path):
            return "Error: Path is not a file"
        
        # Security: Check file size to prevent DoS attacks (limit to 10MB)
        max_file_size = 10 * 1024 * 1024  # 10MB
        if os.path.getsize(abs_path) > max_file_size:
            return "Error: File size exceeds maximum allowed size"
        
        # Read the YAML file with safe loader to prevent arbitrary code execution
        with open(abs_path, 'r', encoding='utf-8') as file:
            # Use SafeLoader instead of Loader to prevent arbitrary code execution
            # This protects against YAML deserialization attacks (CWE-502)
            yaml_content = yaml.load(file, Loader=yaml.SafeLoader)
        
        # Convert to JSON
        json_string = json.dumps(yaml_content, ensure_ascii=False, indent=2)
        
        return json_string
        
    except FileNotFoundError:
        return "Error: File not found"
    except PermissionError:
        return "Error: Permission denied"
    except yaml.YAMLError as e:
        return f"Error: Invalid YAML content - {str(e)}"
    except (TypeError, ValueError) as e:
        return f"Error: Cannot convert to JSON - {str(e)}"
    except UnicodeDecodeError:
        return "Error: File encoding error"
    except Exception as e:
        return f"Error: {str(e)}"