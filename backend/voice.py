"""Voice services for GS420 AI Phase 5.

Optional adapters are used so the core app remains runnable without audio
packages or external API keys.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class SpeechToText:
    provider = "none"

    def transcribe(self, audio_path: str) -> dict[str, Any]:
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        raise RuntimeError(
            "No STT provider is configured. Install/configure an STT adapter "
            "such as faster-whisper in the deployment environment."
        )


class TextToSpeech:
    provider = "none"

    def synthesize(self, text: str, output_path: str, language: str = "en") -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Text cannot be empty.")
        raise RuntimeError(
            "No TTS provider is configured. Install/configure a TTS adapter "
            "such as Piper in the deployment environment."
        )
