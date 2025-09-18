#!/usr/bin/env python3
"""
Claude Code MCP Server with Streaming Support
Uses Context to send progress updates
"""

import os
import sys
import subprocess
import shutil
import asyncio
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Check if Claude Code CLI is installed
CLAUDE_CLI_PATH = shutil.which("claude")
if not CLAUDE_CLI_PATH:
    print("Error: Claude Code CLI not installed", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
mcp = FastMCP("claude-code")

@mcp.tool()
async def claude_execute(
    prompt: str,
    context: Context,
    working_dir: Optional[str] = None,
    allowed_tools: Optional[str] = None
) -> str:
    """Execute Claude Code CLI with progress updates"""
    
    try:
        # Send initial progress
        await context.report_progress(0, 100, "Starting Claude Code CLI...")
        await context.info(f"Executing prompt: {prompt[:100]}...")
        
        # Build command (no -p flag for intermediate output)
        cmd = [CLAUDE_CLI_PATH, prompt]
        if allowed_tools:
            cmd.extend(["--allowedTools", allowed_tools])
        cmd.append("--dangerously-skip-permissions")
        
        cwd = os.path.expanduser(working_dir) if working_dir else os.getcwd()
        
        # Use Popen to stream output
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        
        output_lines = []
        line_count = 0
        
        # Stream stdout line by line
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            
            line_text = line.decode('utf-8').rstrip()
            output_lines.append(line_text)
            line_count += 1
            
            # Send progress updates for each line
            if line_text:
                await context.info(line_text)
                # Update progress (estimate based on typical output)
                progress = min(80, line_count * 5)
                await context.report_progress(progress, 100, f"Processing: {line_text[:50]}...")
        
        # Wait for process to complete
        await process.wait()
        
        await context.report_progress(100, 100, "Completed")
        
        # Return full output
        if process.returncode == 0:
            return '\n'.join(output_lines)
        else:
            stderr = await process.stderr.read()
            return f"Error (exit {process.returncode}): {stderr.decode('utf-8')}"
            
    except asyncio.TimeoutError:
        await context.error("Task timed out after 5 minutes")
        return "Task timed out"
    except Exception as e:
        await context.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"

# Run server
async def run_server(host="127.0.0.1", port=8000):
    """Run the MCP server with CORS"""
    app = mcp.streamable_http_app()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id", "mcp-session-id", "*"]
    )
    
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    
    args = parser.parse_args()
    
    print(f"Claude Code MCP Server with Streaming", file=sys.stderr)
    print(f"======================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}/mcp", file=sys.stderr)
    print(f"", file=sys.stderr)
    
    asyncio.run(run_server(args.host, args.port))