#!/usr/bin/env python3
"""
Scrimba Teaching API Server
Phase 1: Basic REST endpoints with MCP bridge
Following Progressive Enhancement - Ship working version first
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import our MCP bridge
from core.mcp_bridge import MCPBridge

# Phase 1: Simple global bridge (will enhance later)
mcp_bridge = MCPBridge()
executor = ThreadPoolExecutor(max_workers=10)

app = FastAPI(
    title="Scrimba Teaching API",
    description="Bridge traditional apps to Scrimba MCP teaching",
    version="1.0.0"
)

# Enable CORS for React apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Phase 1: Allow all (will restrict later)
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
    
class AgentRequest(BaseModel):
    prompt: str
    use_agent: Optional[bool] = False

# Helper to run blocking MCP calls
async def run_mcp_tool(tool_name: str, arguments: Dict = None):
    """Run MCP tool in thread pool"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        mcp_bridge.call_tool,
        tool_name,
        arguments
    )

# Phase 1 Endpoints: Core teaching functions

@app.on_event("startup")
async def startup():
    """Start MCP bridge on server startup"""
    mcp_bridge.start()
    print("✅ MCP Bridge started")

@app.get("/")
async def health():
    """Health check endpoint"""
    return {
        "status": "ready",
        "service": "Scrimba Teaching API",
        "mcp_connected": mcp_bridge.process is not None
    }

@app.post("/api/teach")
async def teach(request: TeachRequest):
    """Teach a programming concept"""
    try:
        result = await run_mcp_tool("teach", {
            "topic": request.topic,
            "step": request.step
        })
        
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
async def get_challenge(request: ChallengeRequest):
    """Get a coding challenge"""
    try:
        result = await run_mcp_tool("give_challenge", {
            "difficulty": request.difficulty
        })
        
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
    try:
        result = await run_mcp_tool("check_code", {
            "code": request.code
        })
        
        # Determine if code is correct (simple heuristic for Phase 1)
        is_correct = "great" in result.lower() or "correct" in result.lower()
        
        return {
            "success": True,
            "feedback": result,
            "is_correct": is_correct
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/progress")
async def get_progress():
    """Get learning progress"""
    try:
        result = await run_mcp_tool("show_progress", {})
        return {
            "success": True,
            "progress": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Phase 2: Will add Claude CLI agent endpoint
# Phase 3: Will add session management
# Phase 4: Will add WebSocket for real-time
# Phase 5: Will add batch operations
# Phase 6: Will add analytics
# Phase 7: Will add multi-tenant support

@app.on_event("shutdown")
async def shutdown():
    """Clean shutdown"""
    mcp_bridge.stop()
    executor.shutdown()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Scrimba Teaching API")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔧 Phase 1: Basic MCP bridge working")
    uvicorn.run(app, host="0.0.0.0", port=8000)