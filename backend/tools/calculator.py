import ast,operator as op
OPS={ast.Add:op.add,ast.Sub:op.sub,ast.Mult:op.mul,ast.Div:op.truediv,ast.Mod:op.mod,ast.Pow:op.pow,ast.USub:op.neg}
def calculate(expr):
 def e(n):
  if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
  if isinstance(n,ast.BinOp) and type(n.op) in OPS:return OPS[type(n.op)](e(n.left),e(n.right))
  if isinstance(n,ast.UnaryOp) and type(n.op) in OPS:return OPS[type(n.op)](e(n.operand))
  raise ValueError("Only arithmetic is allowed")
 return e(ast.parse(expr,mode="eval").body)
