"""Abstract model interface for GS420 AI."""
from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any

class BaseModel(ABC):
    @abstractmethod
    def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream(self, messages: list[dict[str, str]], **kwargs: Any) -> Generator[str, None, None]:
        raise NotImplementedError

    @abstractmethod
    def info(self) -> dict[str, Any]:
        raise NotImplementedError
