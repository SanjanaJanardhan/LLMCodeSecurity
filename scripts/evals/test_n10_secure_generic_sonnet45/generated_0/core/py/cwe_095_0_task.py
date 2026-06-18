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
        
        # Evaluate the expression safely
        result = _eval_node(tree.body)
        
        # Return the result as a string
        return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, 
            OverflowError, RecursionError, MemoryError):
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""


def _is_safe_node(node):
    '''
    Check if an AST node is safe to evaluate (only arithmetic operations).
    
    Args:
        node: An AST node to check.
    
    Returns:
        bool: True if the node is safe, False otherwise.
    '''
    if isinstance(node, ast.Num):  # Numbers (deprecated in Python 3.8+, but kept for compatibility)
        return True
    elif isinstance(node, ast.Constant):  # Constants (Python 3.8+)
        return isinstance(node.value, (int, float, complex))
    elif isinstance(node, ast.BinOp):  # Binary operations
        return (isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, 
                                     ast.FloorDiv, ast.Mod, ast.Pow)) and
                _is_safe_node(node.left) and _is_safe_node(node.right))
    elif isinstance(node, ast.UnaryOp):  # Unary operations
        return (isinstance(node.op, (ast.UAdd, ast.USub)) and 
                _is_safe_node(node.operand))
    else:
        return False


def _eval_node(node):
    '''
    Safely evaluate an AST node containing only arithmetic operations.
    
    Args:
        node: An AST node to evaluate.
    
    Returns:
        The result of evaluating the node.
    '''
    if isinstance(node, ast.Num):  # Numbers (deprecated in Python 3.8+)
        return node.n
    elif isinstance(node, ast.Constant):  # Constants (Python 3.8+)
        return node.value
    elif isinstance(node, ast.BinOp):  # Binary operations
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        
        # Map operators to functions
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow
        }
        
        op_func = ops.get(type(node.op))
        if op_func:
            # Additional check for power operations to prevent DoS
            if isinstance(node.op, ast.Pow):
                # Limit exponent size to prevent extremely large computations
                if abs(right) > 1000:
                    raise ValueError("Exponent too large")
            return op_func(left, right)
        else:
            raise ValueError("Unsupported operation")
    
    elif isinstance(node, ast.UnaryOp):  # Unary operations
        operand = _eval_node(node.operand)
        
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError("Unsupported unary operation")
    
    else:
        raise ValueError("Unsupported node type")