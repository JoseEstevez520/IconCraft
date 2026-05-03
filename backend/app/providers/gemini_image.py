import base64
import os

import httpx

from app.providers.base import BaseProvider

GEMINI_MODELS = [
    "gemini-2.0-flash-exp-image-generation",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.0-flash-lite",
]


class GeminiImageProvider(BaseProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("IMAGE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60)

    async def _try_model(self, model: str, prompt: str) -> bytes | None:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        body = {
            "contents": [{"parts": [{"text": f"Generate a simple SVG icon of {prompt}. Return ONLY valid SVG code, no explanation, no markdown."}]}],
        }

        resp = await self.client.post(url, json=body)
        if resp.status_code != 200:
            return None

        data = resp.json()
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    return base64.b64decode(part["inlineData"]["data"])
                if "text" in part:
                    text = part["text"].strip()
                    if text.startswith("```svg"):
                        text = text.split("```svg")[1].split("```")[0].strip()
                    elif text.startswith("<svg"):
                        text = text.split("</svg>")[0] + "</svg>"
                    if text.startswith("<svg"):
                        return text.encode()

        return None

    async def generate(self, prompt: str) -> bytes:
        if not self.api_key:
            raise RuntimeError("IMAGE_API_KEY is not set")

        for model in GEMINI_MODELS:
            result = await self._try_model(model, prompt)
            if result:
                return result

        raise RuntimeError("Gemini image generation failed. Try a different provider like flux or openai.")

    async def close(self) -> None:
        await self.client.aclose()
