from pathlib import Path
def test_react_frontend():
 assert Path("frontend/src/App.jsx").exists()
 assert Path("frontend/src/main.jsx").exists()
 assert Path("frontend/package.json").exists()
def test_frontend_has_canonical_tabs():
 t=Path("frontend/src/App.jsx").read_text()
 for x in ["Chat","Coding","Vision","Image","Video","Voice","Agents","Documents","Memory","Settings"]:assert x in t
