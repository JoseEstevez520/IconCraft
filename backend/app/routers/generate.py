from fastapi import APIRouter, HTTPException
from httpx import HTTPStatusError
from pydantic import BaseModel

from app.pipeline.prompt_builder import Style, build_prompt
from app.providers import get_provider
from app.providers.retry import with_retry
from app.pipeline.preprocessor import process_image
from app.pipeline.vectorizer import vectorize
from app.pipeline.optimizer import optimize

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str
    style: Style = "Flat"
    color: str = "#1e1e1e"
    size: int = 64


class GenerateResponse(BaseModel):
    svg: str
    size: int


@router.post("/generate")
async def generate_icon(req: GenerateRequest) -> GenerateResponse:
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    try:
        enhanced = build_prompt(req.prompt, req.style, req.color)
        provider = get_provider()
        try:
            image_data = await with_retry(
                lambda: provider.generate(enhanced),
                max_retries=3,
                base_delay=1.0,
                retryable=lambda e: isinstance(e, (HTTPStatusError, TimeoutError)),
            )
        finally:
            await provider.close()

        img = await process_image(image_data)
        raw_svg = await vectorize(img)
        optimized_svg = await optimize(raw_svg)

        return GenerateResponse(svg=optimized_svg, size=req.size)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
