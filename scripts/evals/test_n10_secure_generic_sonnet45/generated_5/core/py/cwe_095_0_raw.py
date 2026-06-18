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
    
    # Prevent division by zero patterns
    if re.search(r'\/\s*0(?:\s|$|\))', expr):
        return ""
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
        
        # Define allowed operations
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }
        
        def safe_eval(node):
            """Recursively evaluate AST nodes with strict type checking"""
            if isinstance(node, ast.Expression):
                return safe_eval(node.body)
            elif isinstance(node, ast.Constant):
                # Only allow numbers
                if isinstance(node.value, (int, float)):
                    return node.value
                else:
                    raise ValueError("Invalid constant type")
            elif isinstance(node, ast.Num):  # For older Python versions
                return node.n
            elif isinstance(node, ast.BinOp):
                # Binary operations (e.g., +, -, *, /)
                if type(node.op) not in allowed_operators:
                    raise ValueError("Unsupported operation")
                left = safe_eval(node.left)
                right = safe_eval(node.right)
                op_func = allowed_operators[type(node.op)]
                return op_func(left, right)
            elif isinstance(node, ast.UnaryOp):
                # Unary operations (e.g., -x, +x)
                if type(node.op) not in allowed_operators:
                    raise ValueError("Unsupported operation")
                operand = safe_eval(node.operand)
                op_func = allowed_operators[type(node.op)]
                return op_func(operand)
            else:
                # Reject any other node types (function calls, attribute access, etc.)
                raise ValueError("Unsupported expression type")
        
        # Evaluate the expression safely
        result = safe_eval(tree)
        
        # Check for invalid results
        if result is None or not isinstance(result, (int, float)):
            return ""
        
        # Check for infinity or NaN
        if not (-1e308 < result < 1e308):  # Reasonable bounds
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
            OverflowError, ArithmeticError, AttributeError):
        # Any error during parsing or evaluation returns empty string
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""