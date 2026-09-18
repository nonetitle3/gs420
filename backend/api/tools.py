from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from backend.tools.calculator import calculate
from backend.tools.code_runner import run_python
router=APIRouter(prefix="/api/tools",tags=["tools"])
class CalcRequest(BaseModel): expression:str=Field(min_length=1,max_length=500)
class PythonRequest(BaseModel): code:str=Field(min_length=1,max_length=20000)
@router.post("/calculator")
def calculator(x:CalcRequest): return calculate(x.expression)
@router.post("/python")
def python_tool(x:PythonRequest):
    result=run_python(x.code)
    if not result.get("ok") and result.get("error")=="Blocked operation": raise HTTPException(400,result["error"])
    return result
