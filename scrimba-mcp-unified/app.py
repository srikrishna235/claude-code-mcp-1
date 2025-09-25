"""
Scrimba MCP HTTP Server for Render - FINAL VERSION
Copy this to scrimba-mcp-unified/app.py in your GitHub repo
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Scrimba Teaching MCP")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key from environment
API_KEY = os.environ.get("MCP_API_KEY", "scrimba-teaching-secure-key-2024")

@app.get("/")
async def root():
    return {
        "name": "Scrimba Teaching MCP",
        "version": "3.0.2",
        "status": "running",
        "message": "MCP server is active. Use POST /mcp to interact."
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "scrimba-mcp"}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP endpoint - simplified version"""
    # Check API key
    if request.headers.get("X-API-Key") != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    body = await request.json()
    prompt = body.get("prompt", "")
    mode = body.get("mode", "auto")
    
    # Simplified response for testing
    response = {
        "result": {
            "type": "teaching",
            "content": f"Teaching response for: {prompt}",
            "mode": mode,
            "lesson": "This is a placeholder response. Full MCP integration coming soon."
        },
        "status": "success"
    }
    
    return JSONResponse(response)

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            "scrimba_agent",
            "teach", 
            "give_challenge",
            "check_code",
            "visualize_concept",
            "start_project"
        ],
        "status": "Available in full version"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
