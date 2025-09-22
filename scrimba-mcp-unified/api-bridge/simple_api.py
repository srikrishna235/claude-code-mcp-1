#!/usr/bin/env python3
"""
Simple API Server - Direct function calls instead of MCP protocol
Phase 1: Get it working first, optimize later
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import sys

# Add servers to path
sys.path.append('/home/rishabh/Desktop/dev/claude-code-mcp/scrimba-mcp-unified')

# Import teaching functions directly
from servers.teaching.server import teach, give_challenge, check_code, show_progress, next, celebrate

app = FastAPI(
    title="Scrimba Teaching API (Simple)",
    description="Direct bridge to Scrimba teaching functions",
    version="1.0.0"
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

# Endpoints

@app.get("/")
async def health():
    """Health check"""
    return {
        "status": "ready",
        "service": "Scrimba Teaching API (Simple)",
        "method": "direct_import"
    }

@app.post("/api/teach")
async def api_teach(request: TeachRequest):
    """Teach a programming concept"""
    try:
        result = await teach(request.topic, request.step)
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
async def api_challenge(request: ChallengeRequest):
    """Get a coding challenge"""
    try:
        result = await give_challenge(request.difficulty)
        time_limits = {"easy": 60, "medium": 120, "hard": 180}
        return {
            "success": True,
            "challenge": result,
            "time_limit": time_limits.get(request.difficulty, 60)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check")
async def api_check(request: CheckCodeRequest):
    """Check user's code"""
    try:
        result = await check_code(request.code)
        is_correct = "great" in result.lower() or "perfect" in result.lower()
        return {
            "success": True,
            "feedback": result,
            "is_correct": is_correct
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/progress")
async def api_progress():
    """Get progress"""
    try:
        result = await show_progress()
        return {
            "success": True,
            "progress": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/next")
async def api_next():
    """Next lesson"""
    try:
        result = await next()
        return {
            "success": True,
            "lesson": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/celebrate")
async def api_celebrate():
    """Celebrate achievement"""
    try:
        result = await celebrate("progress")
        return {
            "success": True,
            "celebration": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple API Server")
    print("📚 Direct import method - no MCP protocol")
    print("📖 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)