def test_memory_features(tmp_path):
 from backend.core.memory_manager import MemoryManager
 m=MemoryManager(tmp_path/"m.db");m.add_message("s","user","hello world");assert m.history("s")[0]["content"]=="hello world"
 m.add_memory("বাংলা","fact");m.set_preference("language","bn");m.save_prompt("x","hello");assert m.preferences()[0]["key"]=="language";assert m.saved_prompts()[0]["title"]=="x"
 m.clear_session("s");assert m.history("s")==[]
