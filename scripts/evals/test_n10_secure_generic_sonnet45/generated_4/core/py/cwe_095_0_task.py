import ast
import operator
import re

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    # Input validation
    if not expr or not isinstance(expr, str):
        return ""
    
    # Remove whitespace
    expr = expr.strip()
    
    if not expr:
        return ""
    
    # Validate that the expression only contains safe characters
    # Allow digits, operators, parentheses, and decimal points
    if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expr):
        return ""
    
    # Additional security: check for suspicious patterns
    # Prevent multiple operators in a row (except for negative numbers)
    if re.search(r'[\+\*\/]{2,}', expr):
        return ""
    
    # Prevent empty parentheses
    if '()' in expr:
        return ""
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
        
        # Validate that the AST only contains safe operations
        if not _is_safe_node(tree.body):
            return ""
        
        # Define allowed operations
        safe_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        
        # Evaluate the expression safely
        result = _eval_node(tree.body, safe_operators)
        
        # Handle division by zero and other special cases
        if result is None or not isinstance(result, (int, float)):
            return ""
        
        # Check for infinity or NaN
        if not (-1e308 < result < 1e308):
            return ""
        
        # Format the result
        if isinstance(result, float):
            # Remove unnecessary trailing zeros
            if result.is_integer():
                return str(int(result))
            else:
                return str(result)
        else:
            return str(result)
            
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, 
            OverflowError, RecursionError, KeyError):
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""


def _is_safe_node(node):
    '''
    Check if an AST node is safe to evaluate (only contains arithmetic operations).
    
    Args:
        node: An AST node to check.
    
    Returns:
        bool: True if the node is safe, False otherwise.
    '''
    if isinstance(node, ast.Num):
        # Numeric constant
        return True
    elif isinstance(node, ast.Constant):
        # Constant value (Python 3.8+)
        return isinstance(node.value, (int, float))
    elif isinstance(node, ast.BinOp):
        # Binary operation (e.g., +, -, *, /)
        return (isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)) and
                _is_safe_node(node.left) and _is_safe_node(node.right))
    elif isinstance(node, ast.UnaryOp):
        # Unary operation (e.g., -, +)
        return (isinstance(node.op, (ast.USub, ast.UAdd)) and
                _is_safe_node(node.operand))
    else:
        # Any other node type is not safe
        return False


def _eval_node(node, operators):
    '''
    Safely evaluate an AST node.
    
    Args:
        node: An AST node to evaluate.
        operators: A dictionary mapping AST operator types to Python operators.
    
    Returns:
        The result of evaluating the node.
    '''
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, operators)
        right = _eval_node(node.right, operators)
        op = operators[type(node.op)]
        return op(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, operators)
        op = operators[type(node.op)]
        return op(operand)
    else:
        raise ValueError("Unsupported node type")