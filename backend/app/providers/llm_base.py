from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def chat(self, message: str, system_prompt: str | None = None) -> str:
        ...
