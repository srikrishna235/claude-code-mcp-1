#!/usr/bin/env python3
"""
Claude Code CLI as MCP Server - Final Minimalistic Version
Wraps actual Claude Code CLI using FastMCP for simplicity
Following Progressive Enhancement Methodology: Ship Phase 1
"""

import os
import sys
import subprocess
import shutil
from typing import Optional
from mcp.server.fastmcp import FastMCP

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

# Phase 2: Will add specialized tools
# Phase 3: Will add resources for file browsing
# Phase 4: Will add prompts for common workflows
# Phase 5: Will add streaming support

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code CLI as MCP Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    print(f"Claude Code MCP Server (Minimal Version)", file=sys.stderr)
    print(f"========================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}/mcp", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Tool available: claude_execute", file=sys.stderr)
    print(f"  - Takes natural language prompts", file=sys.stderr)
    print(f"  - Executes via Claude Code CLI", file=sys.stderr)
    print(f"  - Returns AI-generated results", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Example prompts:", file=sys.stderr)
    print(f'  "What does this project do?"', file=sys.stderr)
    print(f'  "Add error handling to the main function"', file=sys.stderr)
    print(f'  "Fix the bug in line 42 of server.py"', file=sys.stderr)
    print(f'  "Create a REST API endpoint for users"', file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"Config for Claude Desktop:", file=sys.stderr)
    print(f'{{', file=sys.stderr)
    print(f'  "mcpServers": {{', file=sys.stderr)
    print(f'    "claude-code": {{', file=sys.stderr)
    print(f'      "url": "http://{args.host}:{args.port}/mcp"', file=sys.stderr)
    print(f'    }}', file=sys.stderr)
    print(f'  }}', file=sys.stderr)
    print(f'}}', file=sys.stderr)
    
    # Run with HTTP transport
    # Use streamable-http for production HTTP transport
    mcp.run(transport="streamable-http", mount_path="/mcp")