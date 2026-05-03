import httpx
import pytest
from httpx import ASGITransport

from main import app

transport = ASGITransport(app=app)


@pytest.mark.anyio
async def test_chat_empty():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/chat", json={"message": ""})
        assert resp.status_code == 400


@pytest.mark.anyio
async def test_chat_no_api_key_returns_friendly_message():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/chat", json={"message": "hello"})
        assert resp.status_code == 200
        data = resp.json()
        assert "reply" in data
        assert data["reply"]


@pytest.mark.anyio
async def test_generate_empty_prompt():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/generate", json={"prompt": ""})
        assert resp.status_code == 400


@pytest.mark.anyio
async def test_health():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_mcp_info():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/mcp")
        assert resp.status_code == 200
        data = resp.json()
        assert "tools" in data
        assert len(data["tools"]) == 3


@pytest.mark.anyio
async def test_mcp_unknown_method():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/mcp", json={"method": "unknown"})
        assert resp.status_code == 400
