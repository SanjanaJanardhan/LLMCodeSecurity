import re
import math

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    # Validate and sanitize the input expression
    if not isinstance(expr, str) or not expr.strip():
        return ''

    # Remove any whitespace and non-alphanumeric characters, except for the allowed operators
    allowed_chars = r'[^a-zA-Z0-9\+\-\*/\(\)\.]'
    expr = re.sub(allowed_chars, '', expr)

    try:
        # Evaluate the sanitized expression
        result = str(eval(expr, {'__builtins__': None}, {'math': math}))
    except (ValueError, TypeError, SyntaxError, NameError, AttributeError, ZeroDivisionError):
        # Return an empty string if any error occurs during the evaluation
        return ''

    return result