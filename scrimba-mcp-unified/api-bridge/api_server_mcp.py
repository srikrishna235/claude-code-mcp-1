#!/usr/bin/env python3
"""
Production API Server using proper MCP Client
Uses official MCP SDK's ClientSession with stdio transport
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
from contextlib import asynccontextmanager
from mcp_client_bridge import MCPClientBridge

# Global client instance
mcp_client: Optional[MCPClientBridge] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage MCP client lifecycle"""
    global mcp_client
    # Startup
    mcp_client = MCPClientBridge()
    await mcp_client.connect()
    print("✅ Connected to MCP server")
    
    yield
    
    # Shutdown
    await mcp_client.close()
    print("👋 Disconnected from MCP server")

app = FastAPI(
    title="Scrimba Teaching API",
    description="Production-ready bridge to MCP server",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TeachRequest(BaseModel):
    topic: str
    step: Optional[int] = 1

class ChallengeRequest(BaseModel):
    difficulty: Optional[str] = "easy"
    
class CheckCodeRequest(BaseModel):
    code: str
    
class ProjectRequest(BaseModel):
    project_name: Optional[str] = "passenger_counter"

# API Endpoints

@app.get("/")
async def health():
    """Health check endpoint"""
    return {
        "status": "ready",
        "service": "Scrimba Teaching API",
        "version": "2.0.0",
        "mcp_connected": mcp_client is not None
    }

@app.get("/api/tools")
async def list_tools():
    """List available MCP tools"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        tools = await mcp_client.list_tools()
        return {
            "success": True,
            "tools": tools,
            "count": len(tools)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/teach")
async def teach(request: TeachRequest):
    """Teach a programming concept"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        result = await mcp_client.call_tool(
            "teach", 
            {"topic": request.topic, "step": request.step}
        )
        
        return {
            "success": True,
            "lesson": result,
            "metadata": {
                "topic": request.topic,
                "step": request.step,
                "next_step": request.step + 1,
                "time_to_code_seconds": 60
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/challenge")
async def challenge(request: ChallengeRequest):
    """Get a coding challenge"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        result = await mcp_client.call_tool(
            "give_challenge",
            {"difficulty": request.difficulty}
        )
        
        time_limits = {"easy": 60, "medium": 120, "hard": 180}
        
        return {
            "success": True,
            "challenge": result,
            "time_limit": time_limits.get(request.difficulty, 60)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check")
async def check_code(request: CheckCodeRequest):
    """Check user's code"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        result = await mcp_client.call_tool(
            "check_code",
            {"code": request.code}
        )
        
        # Simple heuristic for correctness
        is_correct = any(word in result.lower() for word in ["great", "perfect", "excellent", "good"])
        
        return {
            "success": True,
            "feedback": result,
            "is_correct": is_correct
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/project/start")
async def start_project(request: ProjectRequest):
    """Start a real project"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        result = await mcp_client.call_tool(
            "start_project",
            {"project_name": request.project_name}
        )
        
        return {
            "success": True,
            "project": result,
            "project_name": request.project_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/progress")
async def get_progress():
    """Get learning progress"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        result = await mcp_client.call_tool("show_progress", {})
        
        return {
            "success": True,
            "progress": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/celebrate")
async def celebrate():
    """Celebrate achievement"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not connected")
    
    try:
        result = await mcp_client.call_tool(
            "celebrate",
            {"achievement": "progress"}
        )
        
        return {
            "success": True,
            "celebration": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Production API Server")
    print("🔧 Using proper MCP Client with stdio transport")
    print("📚 Exactly like Claude Code uses it")
    print("📖 API Docs: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)