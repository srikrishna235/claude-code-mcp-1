#!/usr/bin/env python3
"""Direct test of Claude Code CLI through MCP server"""

import httpx
import json
import asyncio

async def test_claude():
    # First get a session
    async with httpx.AsyncClient() as client:
        # Initialize SSE session
        headers = {"Accept": "text/event-stream"}
        response = await client.get("http://127.0.0.1:8000/mcp", headers=headers)
        session_id = response.headers.get("mcp-session-id")
        print(f"Session ID: {session_id}")
        
        # Call claude_execute tool
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": "Create a file called hello.txt with content 'Testing Claude CLI' and then read it back"
                }
            },
            "id": 1
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": session_id
        }
        
        response = await client.post(
            "http://127.0.0.1:8000/mcp",
            json=request,
            headers=headers,
            timeout=60.0
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    asyncio.run(test_claude())