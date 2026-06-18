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
        # Remove any whitespace from the expression
        expr = expr.strip()

        # Define a regular expression to match valid arithmetic operations
        pattern = r'^[-+*/\d.()]+$'
        if not re.match(pattern, expr):
            return ''

        # Evaluate the expression using the built-in eval() function
        result = str(eval(expr))

        # Return the result as a string
        return result
    except:
        # Return an empty string if any error occurs during the evaluation
        return ''