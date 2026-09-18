# GS420 AI Model Guide

Default general model: `Qwen/Qwen2.5-0.5B-Instruct`.

Optional specialist settings: `GS420_REASONING_MODEL_ID`, `GS420_CODING_MODEL_ID`, `GS420_VISION_MODEL_ID`.

The router tries a configured specialist and falls back to the general model. Use compact/quantized models on low-memory devices. Use suitable GPU hardware for larger vision, image and video models. Check `/api/system/resources` and `/api/system/can-load` before heavy loading.
