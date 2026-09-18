from backend.core.model_router import ModelRouter
def test_all_canonical_tasks_have_candidates():
 router=ModelRouter()
 for task in router.TASKS:
  route=router.route("test",task); assert route.candidates and route.task==task
def test_general_route():
 r=ModelRouter().route("hello"); assert r.task=="general_chat" and r.candidates
