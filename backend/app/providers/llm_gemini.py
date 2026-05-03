import os

import httpx

from app.providers.llm_base import BaseLLMProvider

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class GeminiLLMProvider(BaseLLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=30)

    async def chat(self, message: str, system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "LLM_API_KEY is not configured. Set it in .env to enable AI chat."

        contents: list[dict] = [{"parts": [{"text": message}]}]
        body: dict = {"contents": contents}
        if system_prompt:
            body["system_instruction"] = {"parts": [{"text": system_prompt}]}

        resp = await self.client.post(
            f"{GEMINI_API_URL}?key={self.api_key}",
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    async def close(self) -> None:
        await self.client.aclose()
