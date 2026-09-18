from backend.core.model_router import ModelRouter
def test_tasks():
 r=ModelRouter()
 assert r.classify("write python code")=="coding"
 assert r.classify("গণিতের যুক্তি")=="reasoning"
 assert r.classify("অনুবাদ কর")=="translation"
def test_fallback_candidates():
 r=ModelRouter().route("hello")
 assert r.candidates
 assert r.model==r.candidates[0]
