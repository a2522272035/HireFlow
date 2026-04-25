"""
DeepSeek LLM wrapper using OpenAI-compatible API.
"""

from __future__ import annotations

import json
from typing import AsyncGenerator

from openai import AsyncOpenAI

from app.config import settings


class DeepSeekLLM:
    """DeepSeek LLM wrapper using OpenAI-compatible SDK."""

    def __init__(self) -> None:
        api_key = settings.DEEPSEEK_API_KEY
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not configured")

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
        self.model = getattr(settings, "DEEPSEEK_MODEL", "deepseek-chat")
        self.temperature = getattr(settings, "DEEPSEEK_TEMPERATURE", 0.7)
        self.max_tokens = getattr(settings, "DEEPSEEK_MAX_TOKENS", 2048)

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send chat completion and return response content."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
        )
        return response.choices[0].message.content or ""

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """Send chat completion and stream response chunks."""
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
