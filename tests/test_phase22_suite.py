from pathlib import Path
def test_all_phase_tests_are_present():
 root=Path(__file__).parent
 names={p.name for p in root.glob("test_*.py")}
 required={"test_router.py","test_memory.py","test_coding.py","test_vision.py","test_image_ai.py","test_video_ai.py","test_agents_phase9.py","test_tools_phase10.py","test_document_ai.py","test_pwa.py","test_android_scaffold.py","test_gradio_phase14.py","test_frontend_phase15.py","test_models_phase16.py","test_resource_manager.py","test_colab_phase18.py","test_huggingface_phase19.py","test_security_phase20.py","test_observability_phase21.py"}
 assert required.issubset(names)
