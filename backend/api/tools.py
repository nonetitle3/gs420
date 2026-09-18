from fastapi import APIRouter
from pydantic import BaseModel,Field
from backend.tools.code_runner import run_python
router=APIRouter(prefix="/api/tools",tags=["tools"])
class Code(BaseModel):code:str=Field(min_length=1,max_length=20000)
@router.post("/python")
def python_code(x:Code):return run_python(x.code)
