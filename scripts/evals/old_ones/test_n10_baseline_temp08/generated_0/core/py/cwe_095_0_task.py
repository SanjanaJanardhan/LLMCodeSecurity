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
        # Define a dictionary of supported operators and their corresponding functions
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

        # Use a regular expression to split the expression into operands and operators
        tokens = re.findall(r'\d+|\+|\-|\*|\/', expr)

        # Evaluate the expression using a stack-based approach
        stack = []
        for token in tokens:
            if token in ops:
                b = stack.pop()
                a = stack.pop()
                stack.append(ops[token](a, b))
            else:
                stack.append(int(token))

        # Return the final result as a string
        return str(stack.pop())
    except:
        # Return an empty string if any error occurs
        return ''