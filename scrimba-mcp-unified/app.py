"""
HTTP wrapper for Scrimba MCP - Deploy to Railway
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the MCP server
from scrimba_mcp_unified.server import server, scrimba_agent

app = FastAPI(title="Scrimba Teaching MCP")

# CORS for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
API_KEY = os.environ.get("MCP_API_KEY", "scrimba-teaching-secure-key-2024")

@app.get("/")
async def root():
    return {"name": "Scrimba Teaching MCP", "version": "3.0.2", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP endpoint"""
    # Check API key
    if request.headers.get("X-API-Key") != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    body = await request.json()
    prompt = body.get("prompt", "")
    mode = body.get("mode", "auto")
    
    try:
        result = await scrimba_agent(prompt=prompt, mode=mode)
        return JSONResponse({"result": result, "status": "success"})
    except Exception as e:
        return JSONResponse({"error": str(e), "status": "error"}, status_code=500)

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
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)