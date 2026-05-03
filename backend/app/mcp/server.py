from typing import Any

from httpx import HTTPStatusError

from app.pipeline.prompt_builder import build_prompt
from app.providers import get_provider
from app.providers.retry import with_retry
from app.pipeline.preprocessor import process_image
from app.pipeline.vectorizer import vectorize
from app.pipeline.optimizer import optimize


async def handle_mcp_request(method: str, params: dict[str, Any]) -> dict[str, Any]:
    match method:
        case "generate_icon":
            return await _mcp_generate_icon(params)
        case "optimize_svg":
            return await _mcp_optimize_svg(params)
        case "list_styles":
            return _mcp_list_styles()
        case _:
            raise ValueError(f"Unknown MCP method: {method}")


async def _mcp_generate_icon(params: dict[str, Any]) -> dict[str, Any]:
    prompt = params.get("prompt", "")
    if not prompt:
        raise ValueError("prompt is required")

    style = params.get("style", "Flat")
    color = params.get("color", "#1e1e1e")

    enhanced = build_prompt(prompt, style, color)
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

    return {"svg": optimized_svg}


async def _mcp_optimize_svg(params: dict[str, Any]) -> dict[str, Any]:
    svg = params.get("svg", "")
    if not svg:
        raise ValueError("svg is required")

    optimized = await optimize(svg)
    return {"svg": optimized}


def _mcp_list_styles() -> dict[str, Any]:
    return {"styles": ["Flat", "Outline", "Duotone", "Gradient"]}
