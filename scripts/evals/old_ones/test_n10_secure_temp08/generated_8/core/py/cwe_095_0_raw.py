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
    # Sanitize the input to prevent code injection
    expr = re.sub(r'[^0-9.+\-*/()]', '', expr)

    try:
        # Evaluate the expression using the built-in eval() function
        result = str(eval(expr, {'__builtins__': None}, {'math': math}))
    except (ValueError, TypeError, SyntaxError, NameError, ZeroDivisionError):
        # Return an empty string if any error occurs during the evaluation
        return ''

    return result