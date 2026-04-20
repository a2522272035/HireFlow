from __future__ import annotations

import io
from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.config import settings


class ASREngine(ABC):
    """Abstract base class for ASR (Automatic Speech Recognition) engines."""

    @abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        """Transcribe audio data to text."""
        pass

    @abstractmethod
    async def transcribe_stream(
        self,
        audio_stream: AsyncGenerator[bytes, None],
    ) -> AsyncGenerator[str, None]:
        """Stream transcribe audio data."""
        pass


class WhisperEngine(ASREngine):
    """OpenAI Whisper ASR engine."""

    def __init__(self) -> None:
        self.api_key = settings.OPENAI_API_KEY

    async def transcribe(self, audio_data: bytes) -> str:
        """Transcribe using Whisper API."""
        # TODO: Implement Whisper transcription
        return ""

    async def transcribe_stream(
        self,
        audio_stream: AsyncGenerator[bytes, None],
    ) -> AsyncGenerator[str, None]:
        """Stream transcribe using Whisper."""
        # TODO: Implement streaming transcription
        yield ""


class XunfeiEngine(ASREngine):
    """Xunfei (iFlytek) ASR engine."""

    def __init__(self) -> None:
        self.app_id = settings.XUNFEI_APP_ID
        self.api_key = settings.XUNFEI_API_KEY
        self.api_secret = settings.XUNFEI_API_SECRET

    async def transcribe(self, audio_data: bytes) -> str:
        """Transcribe using Xunfei API."""
        # TODO: Implement Xunfei transcription
        return ""

    async def transcribe_stream(
        self,
        audio_stream: AsyncGenerator[bytes, None],
    ) -> AsyncGenerator[str, None]:
        """Stream transcribe using Xunfei."""
        # TODO: Implement streaming transcription
        yield ""


def get_asr_engine() -> ASREngine:
    """Factory function to get ASR engine instance."""
    provider = settings.ASR_PROVIDER.lower()

    if provider == "xunfei":
        return XunfeiEngine()
    else:
        return WhisperEngine()
