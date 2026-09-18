"""Safe arithmetic tool."""
import ast,operator
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow,ast.Mod:operator.mod,ast.USub:operator.neg,ast.UAdd:operator.pos}
def calculate(expression):
    if len(expression)>500:raise ValueError("Expression too long")
    def ev(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
        if isinstance(n,ast.BinOp) and type(n.op) in OPS:return OPS[type(n.op)](ev(n.left),ev(n.right))
        if isinstance(n,ast.UnaryOp) and type(n.op) in OPS:return OPS[type(n.op)](ev(n.operand))
        raise ValueError("Unsupported expression")
    return {"result":ev(ast.parse(expression,mode="eval").body)}
