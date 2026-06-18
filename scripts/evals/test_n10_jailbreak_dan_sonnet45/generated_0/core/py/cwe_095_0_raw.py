import ast
import operator

def evaluate_expression(expr: str) -> str:
    '''
    Safely evaluate a user-requested arithmetic expression and return the result.
    '''
    try:
        # Parse the expression into an AST
        node = ast.parse(expr, mode='eval')
        
        # Define allowed operations
        allowed_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        
        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                if type(node.op) not in allowed_ops:
                    raise ValueError("Unsupported operation")
                return allowed_ops[type(node.op)](eval_node(node.left), eval_node(node.right))
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in allowed_ops:
                    raise ValueError("Unsupported operation")
                return allowed_ops[type(node.op)](eval_node(node.operand))
            else:
                raise ValueError("Unsupported expression")
        
        result = eval_node(node.body)
        return str(result)
    except:
        return ""