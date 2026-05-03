from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.providers import get_llm_provider

router = APIRouter()

SYSTEM_PROMPT = (
    "You are IconCraft's assistant. You help users create SVG icons. "
    "Answer concisely about icon styles (Flat, Outline, Duotone, Gradient), "
    "sizes (16-256px), colors, and how to use the platform."
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat")
async def chat(req: ChatRequest) -> ChatResponse:
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")

    provider = get_llm_provider()
    try:
        reply = await provider.chat(req.message, SYSTEM_PROMPT)
    finally:
        await provider.close()

    return ChatResponse(reply=reply)
