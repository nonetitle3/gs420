from backend.core.resource_manager import ResourceManager

def test_resource_manager_reports_resources():
    info = ResourceManager().info()
    assert "cpu_count" in info
    assert "profile" in info
    assert info["cpu_count"] >= 1

def test_resource_manager_can_load_small_model():
    result = ResourceManager().can_load(0.01)
    assert "allowed" in result
    assert result["model_gb"] == 0.01
