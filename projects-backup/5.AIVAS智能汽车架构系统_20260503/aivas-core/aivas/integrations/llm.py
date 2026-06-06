"""LLM Provider abstraction — Anthropic Claude API with mock fallback."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from aivas.config import settings


class LLMProvider(ABC):
    """Abstract LLM provider. Switch implementation via settings."""

    @abstractmethod
    async def complete(self, prompt: str, system: str | None = None) -> str:
        """Send a completion request and return the response text."""
        ...

    @abstractmethod
    async def classify_intent(self, message: str, intents: list[str]) -> str:
        """Classify user message into one of the given intents."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...


class MockLLMProvider(LLMProvider):
    """Mock provider for offline development — keyword-based intent matching."""

    @property
    def model_name(self) -> str:
        return "mock/dev"

    async def complete(self, prompt: str, system: str | None = None) -> str:
        return (
            f"[Mock LLM] 收到提示词 ({len(prompt)} chars). "
            "当前为离线开发模式，未接入真实 LLM。请直接通过功能界面操作数据。"
        )

    async def classify_intent(self, message: str, intents: list[str]) -> str:
        msg = message.lower()
        if any(w in msg for w in ("需求", "requirement", "req")):
            return "requirements"
        if any(w in msg for w in ("功能", "function", "func", "bdd")):
            return "functional"
        if any(w in msg for w in ("子系统", "subsystem", "ssc", "sc", "ibd")):
            return "logical"
        if any(w in msg for w in ("ecu", "硬件", "hardware", "物理", "拓扑")):
            return "physical"
        if any(w in msg for w in ("变体", "variant", "标签", "tag", "ple")):
            return "variant"
        if any(w in msg for w in ("基线", "baseline", "发布")):
            return "baseline"
        if any(w in msg for w in ("检查", "验证", "一致性", "validation", "verify")):
            return "verification"
        return "conversational"


class AnthropicProvider(LLMProvider):
    """Production provider using the Anthropic Python SDK (direct API, no proxy)."""

    def __init__(self):
        self._model = settings.llm_model
        self._api_key = settings.llm_api_key
        self._max_tokens = settings.llm_max_tokens

    @property
    def model_name(self) -> str:
        return self._model

    async def complete(self, prompt: str, system: str | None = None) -> str:
        try:
            from anthropic import AsyncAnthropic
        except ImportError:
            return "[Error] anthropic SDK not installed. Run: pip install anthropic"

        client = AsyncAnthropic(api_key=self._api_key)
        messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
        kwargs: dict[str, Any] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        response = await client.messages.create(**kwargs)
        # Anthropic returns list of content blocks; extract first text block
        for block in response.content:
            if block.type == "text":
                return block.text
        return ""

    async def classify_intent(self, message: str, intents: list[str]) -> str:
        prompt = (
            f"将以下用户消息分类为以下意图之一：{', '.join(intents)}。\n"
            f"只回复意图名称，不要解释。\n\n"
            f"用户消息：{message}"
        )
        result = (await self.complete(prompt)).strip().lower()
        for intent in intents:
            if intent.lower() in result:
                return intent
        return "conversational"


def get_llm_provider() -> LLMProvider:
    """Factory: returns AnthropicProvider when API key is set, otherwise MockLLMProvider."""
    if settings.llm_api_key:
        return AnthropicProvider()
    return MockLLMProvider()
