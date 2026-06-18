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

        # Define a regular expression pattern to match valid arithmetic expressions
        pattern = r'^(\-?\d+(?:\.\d+)?)([\+\-\*/])(\-?\d+(?:\.\d+)?)$'

        # Match the expression against the pattern
        match = re.match(pattern, expr)

        if match:
            # Extract the operands and operator from the matched expression
            operand1 = float(match.group(1))
            operator = match.group(2)
            operand2 = float(match.group(3))

            # Perform the arithmetic operation and return the result as a string
            if operator == '+':
                result = str(operand1 + operand2)
            elif operator == '-':
                result = str(operand1 - operand2)
            elif operator == '*':
                result = str(operand1 * operand2)
            elif operator == '/':
                if operand2 == 0:
                    return ''
                result = str(operand1 / operand2)
            return result
        else:
            return ''
    except (ValueError, ZeroDivisionError, TypeError):
        return ''