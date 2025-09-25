"""
Proper MCP Server for Render with HTTP+SSE transport
This follows the actual MCP protocol specification
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os
from typing import Any, Dict
import uuid

app = FastAPI(title="Scrimba MCP Server")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"]
)

# Session management
sessions = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"name": "Scrimba MCP Server", "version": "1.0.0", "protocol": "MCP"}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP endpoint - handles JSON-RPC messages"""
    
    # Check for SSE request
    accept_header = request.headers.get("accept", "")
    wants_sse = "text/event-stream" in accept_header
    
    # Get or create session
    session_id = request.headers.get("Mcp-Session-Id") or str(uuid.uuid4())
    
    # Parse JSON-RPC request
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")
    
    # Handle different MCP methods
    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "1.0.0",
                "serverInfo": {
                    "name": "scrimba-mcp",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }
    
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "teach",
                        "description": "Teach a programming concept",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {"type": "string", "description": "The topic to teach"},
                                "level": {"type": "integer", "description": "Complexity level (1-5)", "default": 1}
                            },
                            "required": ["topic"]
                        }
                    },
                    {
                        "name": "give_challenge",
                        "description": "Give a coding challenge",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"], "default": "easy"}
                            }
                        }
                    },
                    {
                        "name": "check_code",
                        "description": "Check user's code with encouragement",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "description": "The code to check"}
                            },
                            "required": ["code"]
                        }
                    }
                ]
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        # Handle tool calls
        if tool_name == "teach":
            result = {
                "type": "text",
                "text": f"Teaching {tool_args.get('topic', 'programming')} at level {tool_args.get('level', 1)}:\n\nLet's start with the basics..."
            }
        elif tool_name == "give_challenge":
            result = {
                "type": "text",
                "text": f"Here's a {tool_args.get('difficulty', 'easy')} challenge:\n\nWrite a function that..."
            }
        elif tool_name == "check_code":
            result = {
                "type": "text",
                "text": f"Great job! Your code looks good. Here's what I noticed:\n\n{tool_args.get('code', '')[:100]}..."
            }
        else:
            result = {"type": "text", "text": f"Unknown tool: {tool_name}"}
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    else:
        # Unknown method
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }
    
    # Return response (SSE or JSON)
    if wants_sse:
        async def generate():
            yield f"data: {json.dumps(response)}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Mcp-Session-Id": session_id}
        )
    else:
        return Response(
            content=json.dumps(response),
            media_type="application/json",
            headers={"Mcp-Session-Id": session_id}
        )

@app.get("/mcp")
async def mcp_sse_endpoint(request: Request):
    """SSE endpoint for server-initiated messages"""
    session_id = request.headers.get("Mcp-Session-Id", str(uuid.uuid4()))
    
    async def event_generator():
        """Generate SSE events"""
        # Send keepalive
        while True:
            yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
            await asyncio.sleep(30)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Mcp-Session-Id": session_id}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)