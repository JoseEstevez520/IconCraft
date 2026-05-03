from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.mcp.server import handle_mcp_request

router = APIRouter()


class MCPRequest(BaseModel):
    method: str
    params: dict | None = None


class MCPResponse(BaseModel):
    result: dict | None = None
    error: str | None = None


@router.post("/mcp")
async def mcp_endpoint(req: MCPRequest) -> MCPResponse:
    try:
        result = await handle_mcp_request(req.method, req.params or {})
        return MCPResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mcp")
async def mcp_info():
    from app.mcp.tools import get_tool_definitions

    return {
        "protocol": "model-context-protocol",
        "version": "1.0",
        "tools": get_tool_definitions(),
    }
