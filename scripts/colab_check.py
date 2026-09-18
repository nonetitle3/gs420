"""Fail-fast Colab/runtime compatibility check."""
import json

def main():
    from backend.core.resource_manager import ResourceManager
    info=ResourceManager(max_cached_models=1).info()
    print(json.dumps(info,indent=2,ensure_ascii=False))
    if not info.get("cuda"):
        print("WARNING: CUDA GPU is not available; heavy models should not be loaded.")
    else:
        print("CUDA GPU detected:",info.get("gpu"))
        print("Profile:",info.get("profile"))

if __name__=="__main__":
    main()
