import base64
import os

import httpx

from app.providers.base import BaseProvider

OPENAI_API_URL = "https://api.openai.com/v1/images/generations"


class OpenAIProvider(BaseProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("IMAGE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60)

    async def generate(self, prompt: str) -> bytes:
        if not self.api_key:
            raise RuntimeError("IMAGE_API_KEY is not set")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json",
        }

        resp = await self.client.post(OPENAI_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        b64 = data["data"][0].get("b64_json")
        if not b64:
            url = data["data"][0].get("url")
            if url:
                img_resp = await self.client.get(url)
                img_resp.raise_for_status()
                return img_resp.content
            raise RuntimeError(f"OpenAI response missing image data: {data}")

        return base64.b64decode(b64)

    async def close(self) -> None:
        await self.client.aclose()
