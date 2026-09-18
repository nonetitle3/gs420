from fastapi import APIRouter
from pydantic import BaseModel,Field
from backend.tools.calculator import calculate
router=APIRouter(prefix="/api/tools",tags=["tools"])
class CalcRequest(BaseModel):expression:str=Field(min_length=1,max_length=500)
@router.post("/calculator")
def calculator(x:CalcRequest):return calculate(x.expression)
