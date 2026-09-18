"""Hardware-aware resource management for GS420 AI.

The manager is deliberately conservative: it reports capabilities, recommends
profiles, tracks loaded models, and can evict cached model objects. It never
pretends a phone can run a large model just because an API is reachable.
"""
from __future__ import annotations

import gc
import os
import platform
import time
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ResourceProfile:
    name: str
    max_model_gb: float
    preferred_device: str
    heavy_remote: bool
    description: str


@dataclass
class LoadedModel:
    model_id: str
    model_gb: float
    loaded_at: float
    last_used: float


PROFILES = {
    "mobile": ResourceProfile("mobile", 1.5, "cpu", True, "Lightweight/local models only; heavy inference should use a remote backend."),
    "low": ResourceProfile("low", 3.0, "cpu", True, "Conservative CPU profile for limited RAM systems."),
    "mid": ResourceProfile("mid", 6.0, "auto", False, "Mid-range system; prefer quantized or compact models."),
    "high": ResourceProfile("high", 12.0, "cuda", False, "GPU system with enough memory for medium/large models."),
    "colab_t4": ResourceProfile("colab_t4", 10.0, "cuda", False, "Colab-style T4 GPU profile; leave VRAM headroom for runtime overhead."),
}


class ResourceManager:
    def __init__(self, max_cached_models: int = 2):
        self.max_cached_models = max(1, max_cached_models)
        self._loaded: dict[str, LoadedModel] = {}

    def info(self) -> dict[str, Any]:
        ram_total = ram_available = None
        try:
            import psutil
            vm = psutil.virtual_memory()
            ram_total = round(vm.total / (1024 ** 3), 2)
            ram_available = round(vm.available / (1024 ** 3), 2)
        except Exception:
            pass

        cuda = False
        gpu = None
        vram_total = vram_free = None
        try:
            import torch
            cuda = bool(torch.cuda.is_available())
            if cuda:
                gpu = torch.cuda.get_device_name(0)
                free, total = torch.cuda.mem_get_info(0)
                vram_total = round(total / (1024 ** 3), 2)
                vram_free = round(free / (1024 ** 3), 2)
        except Exception:
            pass

        return {
            "platform": platform.system(),
            "machine": platform.machine(),
            "cpu_count": os.cpu_count() or 1,
            "ram_total_gb": ram_total,
            "ram_available_gb": ram_available,
            "cuda": cuda,
            "gpu": gpu,
            "vram_total_gb": vram_total,
            "vram_free_gb": vram_free,
            "profile": self.recommend_profile(),
            "loaded_models": self.loaded_models(),
        }

    def recommend_profile(self) -> str:
        # CUDA + VRAM is the strongest signal for model placement.
        try:
            import torch
            if torch.cuda.is_available():
                free, total = torch.cuda.mem_get_info(0)
                vram = total / (1024 ** 3)
                if vram <= 7:
                    return "colab_t4"
                return "high"
        except Exception:
            pass

        try:
            import psutil
            ram = psutil.virtual_memory().total / (1024 ** 3)
            if ram < 4:
                return "mobile"
            if ram < 8:
                return "low"
            if ram < 16:
                return "mid"
            return "high"
        except Exception:
            return "low"

    def profile(self) -> dict[str, Any]:
        return asdict(PROFILES[self.recommend_profile()])

    def can_load(self, model_gb: float, task: str = "general_chat") -> dict[str, Any]:
        model_gb = max(0.0, float(model_gb))
        profile = PROFILES[self.recommend_profile()]
        available = None
        if task in {"image_generation", "video_generation"} and self.info()["vram_free_gb"] is not None:
            available = self.info()["vram_free_gb"]
        elif self.info()["ram_available_gb"] is not None:
            available = self.info()["ram_available_gb"]

        allowed = model_gb <= profile.max_model_gb
        if available is not None:
            allowed = allowed and model_gb <= max(0.5, available * 0.75)

        return {
            "allowed": allowed,
            "profile": profile.name,
            "model_gb": model_gb,
            "available_gb": available,
            "max_model_gb": profile.max_model_gb,
            "heavy_remote": profile.heavy_remote,
            "reason": "within conservative resource limits" if allowed else "model exceeds the conservative resource budget",
        }

    def register_loaded(self, model_id: str, model_gb: float = 0.0) -> None:
        now = time.time()
        self._loaded[model_id] = LoadedModel(model_id, max(0.0, float(model_gb)), now, now)

    def touch(self, model_id: str) -> None:
        if model_id in self._loaded:
            self._loaded[model_id].last_used = time.time()

    def loaded_models(self) -> list[dict[str, Any]]:
        return [asdict(x) for x in sorted(self._loaded.values(), key=lambda x: x.last_used, reverse=True)]

    def eviction_candidates(self) -> list[str]:
        excess = max(0, len(self._loaded) - self.max_cached_models)
        return [x.model_id for x in sorted(self._loaded.values(), key=lambda x: x.last_used)[:excess]]

    def forget(self, model_id: str) -> None:
        self._loaded.pop(model_id, None)
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

    def unload(self, model_id: str, cache: dict[str, Any]) -> bool:
        if model_id not in cache:
            self.forget(model_id)
            return False
        del cache[model_id]
        self.forget(model_id)
        return True
