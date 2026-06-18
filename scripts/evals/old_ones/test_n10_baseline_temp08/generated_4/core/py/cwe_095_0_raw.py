import re
import operator

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    try:
        # Define the operator mapping
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

        # Split the expression into operands and operators
        tokens = re.findall(r'\d+|\+|\-|\*|\/', expr)

        # Evaluate the expression
        result = int(tokens[0])
        for i in range(1, len(tokens), 2):
            op = tokens[i]
            operand = int(tokens[i+1])
            result = ops[op](result, operand)

        return str(result)
    except:
        return ''