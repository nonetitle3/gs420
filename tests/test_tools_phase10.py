def test_calculator_safe():
 from backend.tools.calculator import calculate
 assert calculate("2+3*4")["result"]==14
def test_calculator_rejects_calls():
 from backend.tools.calculator import calculate
 try:calculate("__import__('os').system('x')")
 except ValueError:assert True
 else:assert False
def test_registry():
 from backend.tools.registry import ToolRegistry,ToolSpec
 r=ToolRegistry();r.register(ToolSpec("x","test",{}, "safe",lambda:1))
 assert r.execute("x")==1
