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
        # Remove any leading/trailing whitespace
        expr = expr.strip()

        # Check if the expression is valid
        if not re.match(r'^[\d\+\-\*/\(\)\.]+$', expr):
            return ''

        # Evaluate the expression
        result = eval(expr)

        # Format the result as a string
        return '{:.2f}'.format(result)
    except:
        # Return an empty string if any error occurs
        return ''