#!/usr/bin/env python3
"""
Claude Code CLI as MCP Server - With CORS Support
Wraps actual Claude Code CLI using FastMCP
"""

import os
import sys
import subprocess
import shutil
from typing import Optional
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request
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
        Claude Code's response with intermediate steps
    """
    try:
        # Build command with stream-json output to capture intermediate steps
        cmd = [CLAUDE_CLI_PATH, prompt]
        
        # Add output format with verbose to capture all events
        cmd.extend(["--output-format", "stream-json", "--verbose"])
        
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
        
        # Parse the stream-json output to extract steps
        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            steps = []
            final_response = ""
            
            for line in output_lines:
                if line.strip():
                    try:
                        event = json.loads(line)
                        event_type = event.get('type', '')
                        
                        # Capture different event types
                        if event_type == 'tool_use':
                            tool_name = event.get('name', 'unknown')
                            steps.append(f"🔧 Using tool: {tool_name}")
                        elif event_type == 'text':
                            text = event.get('text', '').strip()
                            if text:
                                steps.append(f"💭 {text}")
                        elif event_type == 'tool_result':
                            steps.append(f"✅ Tool completed")
                        elif event_type == 'completion':
                            final_response = event.get('completion', '')
                            
                    except json.JSONDecodeError:
                        # If not JSON, it might be regular output
                        if line.strip():
                            steps.append(line)
            
            # Format the response with steps
            if steps:
                response = "## Intermediate Steps:\n"
                for i, step in enumerate(steps, 1):
                    response += f"{i}. {step}\n"
                response += "\n## Final Result:\n"
                response += final_response or "Task completed"
                return response
            else:
                return final_response or result.stdout.strip()
        else:
            return f"Error (exit {result.returncode}): {result.stderr or 'Unknown error'}"
            
    except subprocess.TimeoutExpired:
        return "Task timed out after 5 minutes"
    except Exception as e:
        return f"Error: {str(e)}"

# Create app with CORS support
def create_app():
    """Create Starlette app with CORS and MCP mounted"""
    # Get the streamable HTTP app from FastMCP
    # This needs to be run in an async context with proper lifecycle
    app = Starlette()
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for dev
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id", "mcp-session-id"]
    )
    
    return app

# Simple MCP handler
async def handle_mcp_request(request: Request):
    """Handle MCP JSON-RPC requests"""
    try:
        data = await request.json()
        method = data.get("method")
        
        # Handle initialize
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "claude-code",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {
                            "claude_execute": {
                                "description": "Execute tasks with Claude Code CLI"
                            }
                        }
                    }
                }
            }
            return JSONResponse(response)
        
        # Handle initialized notification
        elif method == "initialized":
            return JSONResponse({"jsonrpc": "2.0", "result": None})
        
        # Handle tool calls
        elif method == "tools/call":
            params = data.get("params", {})
            tool_name = params.get("name")
            
            if tool_name == "claude_execute":
                args = params.get("arguments", {})
                result = await claude_execute(
                    prompt=args.get("prompt", ""),
                    working_dir=args.get("working_dir"),
                    allowed_tools=args.get("allowed_tools")
                )
                
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": result
                        }]
                    }
                })
        
        # Handle tools/list
        elif method == "tools/list":
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "tools": [{
                        "name": "claude_execute",
                        "description": "Execute a task using Claude Code CLI's AI capabilities",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string"},
                                "working_dir": {"type": "string"},
                                "allowed_tools": {"type": "string"}
                            },
                            "required": ["prompt"]
                        }
                    }]
                }
            })
        
        return JSONResponse({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}}, status_code=404)
        
    except Exception as e:
        return JSONResponse({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}, status_code=500)

# Run server with proper lifecycle management
async def run_server(host="127.0.0.1", port=8000):
    """Run the server with CORS support"""
    # Create the app
    app = create_app()
    
    # Add MCP endpoint
    app.add_route("/", handle_mcp_request, methods=["POST"])
    
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code CLI as MCP Server with CORS")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    print(f"Claude Code MCP Server (CORS Enabled)", file=sys.stderr)
    print(f"======================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"CORS enabled for browser access", file=sys.stderr)
    print(f"Terminal UI: http://127.0.0.1:8080", file=sys.stderr)
    
    # Run the server
    asyncio.run(run_server(args.host, args.port))