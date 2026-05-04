import os

import httpx

from app.providers.llm_base import BaseLLMProvider

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


class AnthropicLLMProvider(BaseLLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=30)
        self.model = "claude-3-haiku-20240307"

    async def chat(self, message: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "LLM_API_KEY is not configured. Set it in .env to enable AI chat."

        body: dict = {
            "model": self.model,
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": message}],
        }
        if system_prompt:
            body["system"] = system_prompt

        resp = await self.client.post(
            ANTHROPIC_API_URL,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]

    async def close(self) -> None:
        await self.client.aclose()
