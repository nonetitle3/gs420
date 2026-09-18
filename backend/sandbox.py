"""Compatibility wrapper for the restricted Python runner."""
from backend.tools.code_runner import run_python

class SandboxExecutor:
    def __init__(self,timeout_seconds=5,max_output_chars=12000):
        self.timeout_seconds=timeout_seconds;self.max_output_chars=max_output_chars
    def execute_python(self,code):
        from dataclasses import dataclass
        @dataclass
        class Result:
            success:bool;stdout:str;stderr:str;return_code:int;timed_out:bool
        result=run_python(code,self.timeout_seconds)
        return Result(bool(result.get("ok")),result.get("stdout",""),result.get("stderr",result.get("error","")),int(result.get("returncode",-1)),result.get("error")=="Execution timed out")
