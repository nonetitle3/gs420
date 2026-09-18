from .base import BaseModel
from backend.config import settings

class HuggingFaceModel(BaseModel):
    def __init__(self, model_id, device="auto"):
        self.model_id = model_id
        self.device = device
        self.tokenizer = None
        self.model = None

    def _load(self):
        if self.model:
            return
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        requested = (self.device or "auto").lower()
        use_cuda = requested in {"auto", "cuda"} and torch.cuda.is_available()
        if requested == "cuda" and not use_cuda:
            raise RuntimeError("CUDA requested but no CUDA device is available")

        kwargs = {}
        if settings.model_cache_dir:
            kwargs["cache_dir"] = settings.model_cache_dir
        if settings.hf_token:
            kwargs["token"] = settings.hf_token

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, **kwargs)
        model_kwargs = dict(kwargs)
        if use_cuda:
            model_kwargs["device_map"] = "auto"
            model_kwargs["torch_dtype"] = "auto"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id, **model_kwargs)

    def generate(self, messages, max_new_tokens=256, temperature=.7, top_p=.9, **kw):
        self._load()
        import torch

        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        x = self.tokenizer(prompt, return_tensors="pt")
        if hasattr(self.model, "device"):
            x = {k: v.to(self.model.device) for k, v in x.items()}

        with torch.no_grad():
            y = self.model.generate(
                **x,
                max_new_tokens=max_new_tokens,
                do_sample=temperature > 0,
                temperature=max(.01, temperature),
                top_p=top_p,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        return self.tokenizer.decode(
            y[0][x["input_ids"].shape[1]:],
            skip_special_tokens=True,
        ).strip()
