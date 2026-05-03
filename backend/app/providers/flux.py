import os

import httpx

from app.providers.base import BaseProvider

FLUX_API_URL = "https://api.bfl.ml/v1/image"
FLUX_POLL_URL = "https://api.bfl.ml/v1/get_result"


class FluxProvider(BaseProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("IMAGE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=120)

    async def generate(self, prompt: str) -> bytes:
        if not self.api_key:
            raise RuntimeError("IMAGE_API_KEY is not set")

        headers = {"x-key": self.api_key, "Content-Type": "application/json"}

        payload = {
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "steps": 25,
            "guidance": 3.5,
            "safety_tolerance": 2,
        }

        resp = await self.client.post(FLUX_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        request_id = data.get("id")
        if not request_id:
            raise RuntimeError(f"Flux did not return a request id: {data}")

        result = await self._poll(request_id, headers)
        sample = result.get("sample")
        if not sample:
            raise RuntimeError(f"Flux result missing sample: {result}")

        image_resp = await self.client.get(sample)
        image_resp.raise_for_status()
        return image_resp.content

    async def _poll(self, request_id: str, headers: dict) -> dict:
        import asyncio

        for _ in range(30):
            await asyncio.sleep(1)
            resp = await self.client.get(
                f"{FLUX_POLL_URL}?id={request_id}", headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status")
            if status == "Ready":
                return data
            if status in ("Failed", "Error"):
                raise RuntimeError(f"Flux generation failed: {data}")
        raise TimeoutError("Flux generation timed out")

    async def close(self) -> None:
        await self.client.aclose()
