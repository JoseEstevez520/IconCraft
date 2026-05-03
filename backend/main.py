import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import generate, chat, mcp

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

app = FastAPI(title="IconCraft API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(mcp.router, prefix="/api", tags=["mcp"])


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) if str(exc) else "Internal server error"},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
