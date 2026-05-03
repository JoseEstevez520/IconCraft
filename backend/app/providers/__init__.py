import os

from app.providers.base import BaseProvider
from app.providers.llm_base import BaseLLMProvider

# ── Image providers ──

_image_registry: dict[str, type[BaseProvider]] = {}


def register(name: str, provider: type[BaseProvider]) -> None:
    _image_registry[name.lower()] = provider


def get_provider(name: str | None = None) -> BaseProvider:
    key = (name or os.getenv("IMAGE_PROVIDER", "flux")).lower()
    cls = _image_registry.get(key)
    if not cls:
        available = ", ".join(_image_registry)
        raise KeyError(f"Unknown provider '{key}'. Available: {available}")
    return cls()


from app.providers.flux import FluxProvider
from app.providers.openai import OpenAIProvider
from app.providers.gemini_image import GeminiImageProvider
from app.providers.huggingface import HuggingFaceProvider

register("flux", FluxProvider)
register("openai", OpenAIProvider)
register("gemini", GeminiImageProvider)
register("huggingface", HuggingFaceProvider)

# ── LLM providers ──

_llm_registry: dict[str, type[BaseLLMProvider]] = {}


def register_llm(name: str, provider: type[BaseLLMProvider]) -> None:
    _llm_registry[name.lower()] = provider


def get_llm_provider(name: str | None = None) -> BaseLLMProvider:
    key = (name or os.getenv("LLM_PROVIDER", "openai")).lower()
    cls = _llm_registry.get(key)
    if not cls:
        available = ", ".join(_llm_registry)
        raise KeyError(f"Unknown LLM provider '{key}'. Available: {available}")
    return cls()


from app.providers.llm_openai import OpenAILLMProvider
from app.providers.llm_deepseek import DeepSeekLLMProvider
from app.providers.llm_anthropic import AnthropicLLMProvider
from app.providers.llm_gemini import GeminiLLMProvider

register_llm("openai", OpenAILLMProvider)
register_llm("deepseek", DeepSeekLLMProvider)
register_llm("anthropic", AnthropicLLMProvider)
register_llm("gemini", GeminiLLMProvider)
