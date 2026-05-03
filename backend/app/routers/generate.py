import os
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.pipeline.prompt_builder import Style
from app.providers import get_llm_provider, get_provider

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str
    style: Style = "Flat"
    color: str = "#1e1e1e"
    size: int = 64
    mode: Literal["llm", "pipeline"] | None = None


class GenerateResponse(BaseModel):
    svg: str
    size: int


FALLBACK_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>'

PROMPT_ADAPTER_SYSTEM = (
    "You are an expert at writing prompts for AI image generation models. "
    "Given a user's icon description, style, and color, write a detailed, "
    "optimized prompt for generating a high-quality square icon. "
    "Focus on: clean shapes, transparent background, professional vector icon quality, "
    "centered composition, no text, no watermarks. "
    "Return ONLY the prompt text, no explanations, no markdown."
)


async def _llm_to_svg(req: GenerateRequest) -> str:
    prompt = (
        f"Generate a clean SVG icon for: {req.prompt}. "
        f"Style: {req.style}. Color: {req.color}. "
        f"Use viewBox='0 0 24 24', minimal paths, currentColor or '{req.color}'. "
        f"Return ONLY the raw <svg> tag."
    )
    llm = get_llm_provider()
    try:
        reply = await llm.chat(prompt)
    finally:
        await llm.close()
    return _extract_svg(reply)


async def _pipeline_to_svg(req: GenerateRequest) -> str:
    llm = get_llm_provider()
    try:
        adapted = await llm.chat(
            f"Describe a {req.style} style icon of {req.prompt}. "
            f"Primary color: {req.color}. "
            f"Make it detailed and optimized for image generation.",
            PROMPT_ADAPTER_SYSTEM,
        )
    finally:
        await llm.close()

    provider = get_provider()
    try:
        img_bytes = await provider.generate(adapted)
    finally:
        await provider.close()

    from app.pipeline.preprocessor import process_image
    from app.pipeline.vectorizer import vectorize
    from app.pipeline.optimizer import optimize

    img = await process_image(img_bytes)
    svg = await vectorize(img)
    svg = await optimize(svg)
    return svg


def _extract_svg(reply: str) -> str:
    svg = reply.strip()
    if "```svg" in svg:
        svg = svg.split("```svg")[1].split("```")[0].strip()
    elif "```" in svg:
        svg = svg.split("```")[1].split("```")[0].strip()
    if not svg.startswith("<svg"):
        svg = FALLBACK_SVG
    return svg


@router.post("/generate")
async def generate_icon(req: GenerateRequest) -> GenerateResponse:
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    mode = req.mode or os.getenv("GENERATION_MODE", "llm")

    try:
        if mode == "pipeline":
            svg = await _pipeline_to_svg(req)
        else:
            svg = await _llm_to_svg(req)

        from app.pipeline.optimizer import optimize
        svg = await optimize(svg)

        return GenerateResponse(svg=svg, size=req.size)
    except Exception:
        return GenerateResponse(svg=FALLBACK_SVG, size=req.size)
