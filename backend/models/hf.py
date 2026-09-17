"""Hugging Face causal language-model adapter."""
from __future__ import annotations
import threading
from collections.abc import Generator
from typing import Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from backend.config import Settings
from backend.models.base import BaseModel

class HuggingFaceModel(BaseModel):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_id = settings.model_id
        self.requested_device = settings.device.lower()
        self.tokenizer = None
        self.model = None
        self.device = self._select_device()
        self._load_lock = threading.Lock()

    def _select_device(self) -> str:
        if self.requested_device == "cpu":
            return "cpu"
        if self.requested_device == "cuda":
            if not torch.cuda.is_available():
                raise RuntimeError("GS420_DEVICE=cuda was requested, but CUDA is not available.")
            return "cuda"
        if self.requested_device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        raise ValueError("Invalid GS420_DEVICE value. Use: auto, cpu, or cuda.")

    def _load(self) -> None:
        if self.model is not None and self.tokenizer is not None:
            return
        with self._load_lock:
            if self.model is not None and self.tokenizer is not None:
                return
            token_kwargs: dict[str, Any] = {}
            if self.settings.hf_token:
                token_kwargs["token"] = self.settings.hf_token
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, **token_kwargs)
            model_kwargs: dict[str, Any] = {}
            if self.settings.hf_token:
                model_kwargs["token"] = self.settings.hf_token
            if self.device == "cuda":
                model_kwargs["torch_dtype"] = torch.float16
            self.model = AutoModelForCausalLM.from_pretrained(self.model_id, **model_kwargs)
            self.model.to(self.device)
            self.model.eval()
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

    def _build_inputs(self, messages: list[dict[str, str]]) -> dict[str, torch.Tensor]:
        self._load()
        assert self.tokenizer is not None
        try:
            prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        except Exception:
            prompt = "\n".join(
                f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages
            ) + "\nassistant:"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        return {key: value.to(self.device) for key, value in inputs.items()}

    def _generation_kwargs(self, inputs: dict[str, torch.Tensor], **kwargs: Any) -> dict[str, Any]:
        assert self.tokenizer is not None
        max_new_tokens = int(kwargs.get("max_new_tokens", self.settings.max_new_tokens))
        temperature = float(kwargs.get("temperature", self.settings.temperature))
        top_p = float(kwargs.get("top_p", self.settings.top_p))
        generation: dict[str, Any] = {
            **inputs,
            "max_new_tokens": max_new_tokens,
            "top_p": top_p,
            "do_sample": temperature > 0,
            "pad_token_id": self.tokenizer.pad_token_id,
            "eos_token_id": self.tokenizer.eos_token_id,
        }
        if temperature > 0:
            generation["temperature"] = temperature
        return generation

    def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        self._load()
        assert self.model is not None and self.tokenizer is not None
        inputs = self._build_inputs(messages)
        with torch.inference_mode():
            output_ids = self.model.generate(**self._generation_kwargs(inputs, **kwargs))
        input_length = inputs["input_ids"].shape[-1]
        generated_ids = output_ids[0, input_length:]
        return self.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    def stream(self, messages: list[dict[str, str]], **kwargs: Any) -> Generator[str, None, None]:
        self._load()
        assert self.model is not None and self.tokenizer is not None
        inputs = self._build_inputs(messages)
        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )
        generation_kwargs = self._generation_kwargs(inputs, **kwargs)
        generation_kwargs["streamer"] = streamer
        errors: list[BaseException] = []

        def run_generation() -> None:
            try:
                with torch.inference_mode():
                    self.model.generate(**generation_kwargs)
            except BaseException as exc:
                errors.append(exc)

        thread = threading.Thread(target=run_generation, daemon=True)
        thread.start()
        try:
            for chunk in streamer:
                if chunk:
                    yield chunk
            thread.join()
            if errors:
                raise RuntimeError("Hugging Face model generation failed.") from errors[0]
        finally:
            pass

    def info(self) -> dict[str, Any]:
        gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        return {
            "provider": "huggingface",
            "model_id": self.model_id,
            "device": self.device,
            "cuda_available": torch.cuda.is_available(),
            "gpu_name": gpu_name,
            "loaded": self.model is not None,
        }
