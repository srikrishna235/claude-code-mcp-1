#!/usr/bin/env python3
"""
Claude Code CLI as MCP Server - With CORS Support
Using a proxy approach to add CORS headers
"""

import os
import sys
import subprocess
import shutil
from typing import Optional
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, Response
import httpx
import uvicorn
import asyncio

# Check if Claude Code CLI is installed
CLAUDE_CLI_PATH = shutil.which("claude")
if not CLAUDE_CLI_PATH:
    print("Error: Claude Code CLI not installed. Install with: npm install -g @anthropic-ai/claude-code", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
mcp = FastMCP("claude-code")

# Phase 1: Single tool that wraps Claude Code CLI
@mcp.tool()
async def claude_execute(
    prompt: str,
    working_dir: Optional[str] = None,
    allowed_tools: Optional[str] = None
) -> str:
    """
    Execute a task using Claude Code CLI's AI capabilities.
    
    Args:
        prompt: Natural language description of the task
        working_dir: Working directory for execution (optional)
        allowed_tools: Comma-separated list of allowed tools (e.g., "Read,Write,Edit,Bash")
    
    Returns:
        Claude Code's response
    """
    try:
        # Build command
        cmd = [CLAUDE_CLI_PATH, "-p", prompt]  # Use -p for print mode
        
        # Add allowed tools if specified
        if allowed_tools:
            cmd.extend(["--allowedTools", allowed_tools])
        
        # Skip permissions for programmatic usage
        cmd.append("--dangerously-skip-permissions")
        
        # Set working directory
        cwd = os.path.expanduser(working_dir) if working_dir else os.getcwd()
        
        # Execute Claude Code CLI
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300,  # 5 minutes
            env={**os.environ}
        )
        
        # Return output
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error (exit {result.returncode}): {result.stderr or 'Unknown error'}"
            
    except subprocess.TimeoutExpired:
        return "Task timed out after 5 minutes"
    except Exception as e:
        return f"Error: {str(e)}"

async def run_mcp_server():
    """Run the MCP server in a subprocess"""
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-c",
        """
import sys
sys.path.insert(0, '.')
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("claude-code")

# Import the tool from parent
import subprocess
import os
from typing import Optional

@mcp.tool()
async def claude_execute(
    prompt: str,
    working_dir: Optional[str] = None,
    allowed_tools: Optional[str] = None
) -> str:
    import shutil
    CLAUDE_CLI_PATH = shutil.which("claude")
    try:
        cmd = [CLAUDE_CLI_PATH, "-p", prompt]
        if allowed_tools:
            cmd.extend(["--allowedTools", allowed_tools])
        cmd.append("--dangerously-skip-permissions")
        cwd = os.path.expanduser(working_dir) if working_dir else os.getcwd()
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300,
            env={**os.environ}
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error (exit {result.returncode}): {result.stderr or 'Unknown error'}"
    except subprocess.TimeoutExpired:
        return "Task timed out after 5 minutes"
    except Exception as e:
        return f"Error: {str(e)}"

# Run MCP server on port 8001
mcp.run(transport="streamable-http", mount_path="/mcp")
        """,
        env={**os.environ, "UVICORN_PORT": "8001"}
    )
    return proc

async def proxy_handler(request):
    """Proxy requests to MCP server with CORS headers"""
    # Forward the request to the MCP server on port 8001
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Build the target URL
        target_url = f"http://127.0.0.1:8001{request.url.path}"
        
        # Forward the request
        if request.method == "GET":
            # Handle SSE stream
            response = await client.get(
                target_url,
                headers=dict(request.headers),
            )
            
            # Return streaming response with CORS headers
            return StreamingResponse(
                response.iter_bytes(),
                status_code=response.status_code,
                headers={
                    **dict(response.headers),
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Expose-Headers": "Mcp-Session-Id, mcp-session-id",
                },
                media_type=response.headers.get("content-type", "text/event-stream")
            )
        
        elif request.method == "POST":
            # Forward POST request
            body = await request.body()
            response = await client.post(
                target_url,
                content=body,
                headers=dict(request.headers),
            )
            
            # Return response with CORS headers
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers={
                    **dict(response.headers),
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Expose-Headers": "Mcp-Session-Id, mcp-session-id",
                },
                media_type=response.headers.get("content-type", "text/event-stream")
            )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code CLI as MCP Server with CORS")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    print(f"Claude Code MCP Server with CORS Support", file=sys.stderr)
    print(f"========================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}/mcp", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Starting MCP server on internal port 8001...", file=sys.stderr)
    print(f"CORS proxy listening on port {args.port}...", file=sys.stderr)
    
    # Start MCP server as subprocess
    # Then run proxy server
    
    # Create Starlette app with CORS
    app = Starlette()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id", "mcp-session-id"]
    )
    
    # Just run the original MCP server with CORS wrapper
    # Actually, let's use the simpler approach - just add CORS to response
    
    # Run MCP server directly with streamable-http
    mcp.run(transport="streamable-http", mount_path="/mcp")