import ast
import operator

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
    
    # Remove whitespace and check for empty string
    expr = expr.strip()
    if not expr:
        return ""
    
    # Remove null bytes that could be used for injection
    expr = expr.replace('\0', '')
    
    # Define allowed operators for safe evaluation
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }
    
    def safe_eval(node):
        """
        Recursively evaluate AST nodes in a safe manner.
        Only allows numbers, arithmetic operators, and basic expressions.
        """
        if isinstance(node, ast.Constant):
            # Handle constant values (numbers)
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Only numeric constants allowed")
        
        elif isinstance(node, ast.Num):
            # Handle numbers (for older Python versions)
            if isinstance(node.n, (int, float)):
                return node.n
            else:
                raise ValueError("Only numeric values allowed")
        
        elif isinstance(node, ast.BinOp):
            # Handle binary operations (e.g., a + b, a * b)
            if type(node.op) not in allowed_operators:
                raise ValueError("Operator not allowed")
            
            left = safe_eval(node.left)
            right = safe_eval(node.right)
            op_func = allowed_operators[type(node.op)]
            
            # Prevent division by zero
            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
                raise ValueError("Division by zero")
            
            # Prevent excessively large power operations
            if isinstance(node.op, ast.Pow):
                if abs(right) > 1000:
                    raise ValueError("Exponent too large")
            
            return op_func(left, right)
        
        elif isinstance(node, ast.UnaryOp):
            # Handle unary operations (e.g., -5, +3)
            if type(node.op) not in allowed_operators:
                raise ValueError("Operator not allowed")
            
            operand = safe_eval(node.operand)
            op_func = allowed_operators[type(node.op)]
            return op_func(operand)
        
        elif isinstance(node, ast.Expression):
            # Handle the root Expression node
            return safe_eval(node.body)
        
        else:
            # Reject any other node types (function calls, attribute access, etc.)
            raise ValueError("Invalid expression type")
    
    try:
        # Parse the expression into an AST
        # Use mode='eval' to only allow expressions, not statements
        parsed = ast.parse(expr, mode='eval')
        
        # Evaluate the parsed AST safely
        result = safe_eval(parsed)
        
        # Convert result to string
        # Handle floating point results
        if isinstance(result, float):
            # Check for infinity or NaN
            if not (result != result or result == float('inf') or result == float('-inf')):
                return str(result)
            else:
                return ""
        else:
            return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, 
            OverflowError, ArithmeticError):
        # Handle any errors during parsing or evaluation
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""