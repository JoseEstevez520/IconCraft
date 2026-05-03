import os

import httpx

from app.providers.llm_base import BaseLLMProvider

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


class DeepSeekLLMProvider(BaseLLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=30)
        self.model = "deepseek-chat"

    async def chat(self, message: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "LLM_API_KEY is not configured. Set it in .env to enable AI chat."

        messages: list[dict] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        resp = await self.client.post(
            DEEPSEEK_API_URL,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": messages, "max_tokens": 300},
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    async def close(self) -> None:
        await self.client.aclose()
