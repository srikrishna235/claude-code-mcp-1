#!/usr/bin/env python3
"""
Claude Code CLI as MCP Server - With CORS Support (No Validation)
Wraps actual Claude Code CLI using FastMCP without parameter validation
"""

import os
import sys
import subprocess
import shutil
from typing import Optional, Any
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import json

# Check if Claude Code CLI is installed
CLAUDE_CLI_PATH = shutil.which("claude")
if not CLAUDE_CLI_PATH:
    print("Error: Claude Code CLI not installed. Install with: npm install -g @anthropic-ai/claude-code", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
mcp = FastMCP("claude-code")

# Raw tool that accepts any arguments
@mcp.tool()
async def claude_execute(**kwargs) -> str:
    """
    Execute a task using Claude Code CLI's AI capabilities.
    Accepts any arguments to bypass validation.
    """
    # Extract expected arguments with defaults
    prompt = kwargs.get('prompt', '')
    working_dir = kwargs.get('working_dir', None)
    allowed_tools = kwargs.get('allowed_tools', None)
    
    if not prompt:
        return "Error: 'prompt' is required"
    
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

# Run server with proper lifecycle management
async def run_server(host="127.0.0.1", port=8000):
    """Run the server with CORS support"""
    # Get the MCP ASGI app directly (it has its own lifecycle management)
    app = mcp.streamable_http_app()
    
    # Add CORS middleware to the MCP app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for dev
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id", "mcp-session-id"]
    )
    
    # Run the server (streamable_http_app manages its own session lifecycle)
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code CLI as MCP Server with CORS")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    print(f"Claude Code MCP Server (No Validation)", file=sys.stderr)
    print(f"========================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}/mcp", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"CORS enabled for browser access", file=sys.stderr)
    print(f"Parameter validation bypassed with **kwargs", file=sys.stderr)
    
    # Run the server
    asyncio.run(run_server(args.host, args.port))