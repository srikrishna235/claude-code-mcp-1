#!/usr/bin/env python3
"""
CORS Proxy for MCP Server
Adds CORS headers to MCP server responses for browser access
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import asyncio

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # Expose all headers including Mcp-Session-Id
)

# MCP server URL (running on port 8001)
MCP_SERVER_URL = "http://127.0.0.1:8001"

@app.api_route("/{path:path}", methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    """Proxy all requests to MCP server with CORS headers"""
    
    # Build target URL
    target_url = f"{MCP_SERVER_URL}/{path}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get request body
        body = await request.body() if request.method in ["POST", "PUT"] else None
        
        # Forward headers (except host)
        headers = dict(request.headers)
        headers.pop("host", None)
        
        # Make request to MCP server
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body
        )
        
        # Return response with all headers preserved
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type", "application/json")
        )

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="CORS Proxy for MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Proxy port")
    parser.add_argument("--mcp-port", type=int, default=8001, help="MCP server port")
    
    args = parser.parse_args()
    
    # Update MCP server URL
    MCP_SERVER_URL = f"http://127.0.0.1:{args.mcp_port}"
    
    print(f"CORS Proxy for MCP Server", file=sys.stderr)
    print(f"========================", file=sys.stderr)
    print(f"Proxy listening on: http://127.0.0.1:{args.port}", file=sys.stderr)
    print(f"Forwarding to MCP: {MCP_SERVER_URL}", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Browser can now connect to http://127.0.0.1:{args.port}/mcp", file=sys.stderr)
    
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="info")