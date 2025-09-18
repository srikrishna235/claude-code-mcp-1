#!/usr/bin/env python3
"""
Claude Code MCP Server with Real-time Streaming
Sends progressive updates as Claude CLI executes
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
    """
    Execute Claude Code CLI with real-time streaming updates.
    Sends notifications as Claude processes the request.
    """
    try:
        # Send initial notification
        await context.info(f"🚀 Starting Claude Code CLI...")
        await context.report_progress(0, 100, "Initializing...")
        
        # Build command WITHOUT stream-json (it doesn't actually stream)
        # Remove -p for interactive mode that shows real progress
        cmd = [CLAUDE_CLI_PATH, prompt]
        
        if allowed_tools:
            cmd.extend(["--allowedTools", allowed_tools])
        
        cmd.append("--dangerously-skip-permissions")
        
        cwd = os.path.expanduser(working_dir) if working_dir else os.getcwd()
        
        # Create subprocess for streaming output
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        
        # Track progress
        total_steps = 10  # Estimate
        current_step = 0
        output_buffer = []
        
        # Read stdout line by line (interactive mode outputs here)
        while True:
            line = await process.stdout.readline()
            if not line:
                break
                
            line_text = line.decode('utf-8').strip()
            if not line_text:
                continue
            
            # Send each line as progress (no JSON parsing needed)
            await context.info(line_text)
            output_buffer.append(line_text)
        
        # All the JSON parsing code below is now obsolete
        # since we're not using stream-json format anymore
        """
                    # Claude's response
                    msg = event.get('message', {})
                    content = msg.get('content', [])
                    
                    for item in content:
                        if item.get('type') == 'text':
                            text = item.get('text', '')
                            if text:
                                await context.info(f"💭 {text}")
                                output_buffer.append(text)
                                
                        elif item.get('type') == 'tool_use':
                            tool_name = item.get('name')
                            tool_input = item.get('input', {})
                            current_step += 1
                            
                            # Send progress update
                            progress = min(90, (current_step / total_steps) * 100)
                            await context.report_progress(progress, 100, f"Using tool: {tool_name}")
                            
                            # Send detailed tool info
                            if tool_name == 'Write':
                                file_path = tool_input.get('file_path', '')
                                await context.info(f"📝 Creating file: {file_path}")
                                output_buffer.append(f"[Creating file: {file_path}]")
                                
                            elif tool_name == 'Read':
                                file_path = tool_input.get('file_path', '')
                                await context.info(f"📖 Reading file: {file_path}")
                                output_buffer.append(f"[Reading file: {file_path}]")
                                
                            elif tool_name == 'Bash':
                                command = tool_input.get('command', '')
                                desc = tool_input.get('description', '')
                                await context.info(f"💻 Running: {desc or command[:50]}")
                                output_buffer.append(f"[Running: {command}]")
                                
                            elif tool_name == 'Edit':
                                file_path = tool_input.get('file_path', '')
                                await context.info(f"✏️ Editing file: {file_path}")
                                output_buffer.append(f"[Editing file: {file_path}]")
                                
                elif event_type == 'user':
                    # Tool results
                    msg = event.get('message', {})
                    content = msg.get('content', [])
                    
                    for item in content:
                        if item.get('type') == 'tool_result':
                            result_text = item.get('content', '')
                            if result_text:
                                # Truncate long results for notifications
                                if len(result_text) > 200:
                                    summary = result_text[:197] + "..."
                                else:
                                    summary = result_text
                                await context.debug(f"→ {summary}")
                                output_buffer.append(f"  → {summary}")
                                
                elif event_type == 'result':
                    # Final result
                    final = event.get('result', '')
                    if final:
                        await context.info(f"✅ Complete: {final[:200]}")
                        output_buffer.append(f"\n{final}")
                        
                elif event_type == 'system':
                    # System messages (initialization, etc)
                    subtype = event.get('subtype')
                    if subtype == 'init':
                        await context.debug(f"System initialized with tools: {', '.join(event.get('tools', []))[:100]}")
        """
                    
        # Wait for process to complete
        await process.wait()
        
        # Send completion progress
        await context.report_progress(100, 100, "Completed")
        
        # Return formatted output
        if process.returncode == 0:
            result = '\n'.join(output_buffer)
            await context.info("✨ Task completed successfully")
            return result if result else "Task completed (no output)"
        else:
            stderr = await process.stderr.read()
            error_msg = stderr.decode('utf-8') if stderr else 'Unknown error'
            await context.error(f"Process failed: {error_msg[:200]}")
            return f"Error (exit {process.returncode}): {error_msg}"
            
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
    
    print(f"Claude Code MCP Server - Real-time Streaming", file=sys.stderr)
    print(f"=============================================", file=sys.stderr)
    print(f"Claude CLI: {CLAUDE_CLI_PATH}", file=sys.stderr)
    print(f"Endpoint: http://{args.host}:{args.port}/mcp", file=sys.stderr)
    print(f"Features: Progressive updates via Context notifications", file=sys.stderr)
    print(f"", file=sys.stderr)
    
    asyncio.run(run_server(args.host, args.port))