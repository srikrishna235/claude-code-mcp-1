#!/usr/bin/env python3
"""
Final Claude Code MCP Server with Real-time Streaming
Uses FastMCP Context for progressive updates
"""

import os
import sys
import subprocess
import shutil
import asyncio
import json
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Check Claude CLI
CLAUDE_CLI_PATH = shutil.which("claude")
if not CLAUDE_CLI_PATH:
    print("Error: Claude Code CLI not installed", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("claude-code")

@mcp.tool()
async def claude_execute(
    prompt: str,
    ctx: Context,  # Required for streaming
    working_dir: Optional[str] = None,
    allowed_tools: Optional[str] = None
) -> str:
    """Execute Claude Code with real-time streaming of intermediate steps"""
    
    try:
        # Build command
        cmd = [CLAUDE_CLI_PATH, "-p", prompt, "--output-format", "stream-json", "--verbose"]
        if allowed_tools:
            cmd.extend(["--allowedTools", allowed_tools])
        cmd.append("--dangerously-skip-permissions")
        
        cwd = os.path.expanduser(working_dir) if working_dir else os.getcwd()
        
        # Start process asynchronously for streaming
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        
        await ctx.report_progress(0, 100, "Starting Claude Code...")
        
        output_lines = []
        progress = 0
        
        # Stream stdout line by line
        async for line_bytes in process.stdout:
            line = line_bytes.decode('utf-8').rstrip()
            if not line:
                continue
                
            try:
                event = json.loads(line)
                event_type = event.get('type')
                
                if event_type == 'assistant':
                    msg = event.get('message', {})
                    content = msg.get('content', [])
                    for item in content:
                        if item.get('type') == 'text':
                            text = item.get('text', '')
                            await ctx.info(text)  # Stream text in real-time
                            output_lines.append(text)
                        elif item.get('type') == 'tool_use':
                            tool_name = item.get('name')
                            tool_input = item.get('input', {})
                            
                            # Stream tool usage in real-time
                            if tool_name == 'Write':
                                await ctx.info(f"📝 Creating file: {tool_input.get('file_path', '')}")
                                output_lines.append(f"[Creating file: {tool_input.get('file_path', '')}]")
                            elif tool_name == 'Read':
                                await ctx.info(f"📖 Reading file: {tool_input.get('file_path', '')}")
                                output_lines.append(f"[Reading file: {tool_input.get('file_path', '')}]")
                            elif tool_name == 'Bash':
                                cmd_text = tool_input.get('command', '')
                                await ctx.info(f"💻 Running: {cmd_text[:100]}")
                                output_lines.append(f"[Running: {cmd_text}]")
                            elif tool_name == 'Edit':
                                await ctx.info(f"✏️ Editing file: {tool_input.get('file_path', '')}")
                                output_lines.append(f"[Editing file: {tool_input.get('file_path', '')}]")
                            
                            progress = min(progress + 10, 80)
                            await ctx.report_progress(progress, 100, f"Using {tool_name}...")
                            
                elif event_type == 'user':
                    # Tool results
                    msg = event.get('message', {})
                    content = msg.get('content', [])
                    for item in content:
                        if item.get('type') == 'tool_result':
                            result_text = item.get('content', '')
                            if result_text and len(result_text) < 200:
                                await ctx.info(f"→ {result_text}")
                                output_lines.append(f"  → {result_text}")
                                
                elif event_type == 'result':
                    # Final result
                    final = event.get('result', '')
                    if final:
                        output_lines.append(f"\n{final}")
                        
            except json.JSONDecodeError:
                pass  # Skip non-JSON lines
        
        # Wait for process completion
        await process.wait()
        
        await ctx.report_progress(100, 100, "Completed")
        
        if process.returncode == 0:
            return '\n'.join(output_lines)
        else:
            stderr = await process.stderr.read()
            return f"Error: {stderr.decode('utf-8')}"
            
    except Exception as e:
        await ctx.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"

# Run server
async def run_server(host="127.0.0.1", port=8000):
    app = mcp.streamable_http_app()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
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
    
    print(f"Claude Code MCP Server (Final - with Streaming)", file=sys.stderr)
    print(f"===============================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}/mcp", file=sys.stderr)
    print(f"✅ Real-time streaming enabled via Context", file=sys.stderr)
    print(f"", file=sys.stderr)
    
    asyncio.run(run_server(args.host, args.port))