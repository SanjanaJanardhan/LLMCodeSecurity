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
        
        # Validate that the expression only contains allowed characters
        # Allow digits, operators (+, -, *, /, //, %, **), parentheses, and whitespace
        allowed_chars = set("0123456789+-*/%() .")
        if not all(c in allowed_chars for c in expr):
            return ""
        
        # Evaluate the expression using Python's eval with restricted scope
        # This is safe because we've validated the characters
        result = eval(expr)
        
        # Convert result to string
        # Handle float results that are whole numbers
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            else:
                return str(result)
        else:
            return str(result)
    
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError, NameError, KeyError):
        # Return empty string for any evaluation errors
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""