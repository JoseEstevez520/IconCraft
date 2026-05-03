import asyncio
import io
import os
from concurrent.futures import ThreadPoolExecutor

from huggingface_hub import InferenceClient

from app.providers.base import BaseProvider

_pool = ThreadPoolExecutor(1)


class HuggingFaceProvider(BaseProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("IMAGE_API_KEY", "")
        self.client = InferenceClient(token=self.api_key) if self.api_key else None

    async def generate(self, prompt: str) -> bytes:
        if not self.api_key or not self.client:
            raise RuntimeError("IMAGE_API_KEY is not set")

        loop = asyncio.get_running_loop()
        image = await loop.run_in_executor(
            _pool,
            lambda: self.client.text_to_image(
                prompt,
                model="black-forest-labs/FLUX.1-schnell",
            ),
        )
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return buf.getvalue()

    async def close(self) -> None:
        pass
