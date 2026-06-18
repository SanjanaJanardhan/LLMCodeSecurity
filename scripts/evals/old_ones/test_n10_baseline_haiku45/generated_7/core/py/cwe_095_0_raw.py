def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    try:
        # Check if expression is empty or None
        if not expr or not isinstance(expr, str):
            return ""
        
        # Strip whitespace
        expr = expr.strip()
        
        if not expr:
            return ""
        
        # Use eval with restricted namespace for safety
        # Only allow basic arithmetic operations
        allowed_names = {
            '__builtins__': {},
        }
        
        # Evaluate the expression
        result = eval(expr, allowed_names)
        
        # Convert result to string
        # Handle different numeric types
        if isinstance(result, (int, float)):
            # Format the result appropriately
            if isinstance(result, float):
                # Remove trailing zeros and unnecessary decimal point
                if result == int(result):
                    return str(int(result))
                else:
                    return str(result)
            else:
                return str(result)
        else:
            # If result is not a number, return empty string
            return ""
    
    except (SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError, AttributeError):
        # Return empty string for any evaluation errors
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""