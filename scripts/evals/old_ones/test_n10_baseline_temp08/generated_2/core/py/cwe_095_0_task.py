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
    try:
        # Remove whitespace from the expression
        expr = expr.strip()

        # Define a regular expression pattern to match valid arithmetic expressions
        pattern = r'^(\-?\d+(\.\d+)?)([\+\-\*/](\-?\d+(\.\d+)?)){0,}$'

        # Check if the expression matches the pattern
        if re.match(pattern, expr):
            # Evaluate the expression using the eval() function
            result = str(eval(expr))
            return result
        else:
            return ''
    except:
        return ''