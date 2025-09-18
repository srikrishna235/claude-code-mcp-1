#!/usr/bin/env python3
"""Test MCP server for streaming/intermediate outputs"""

import httpx
import json
import asyncio

async def test_mcp_streaming():
    """Test the MCP server with a multi-step task"""
    
    # First, create a session
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # Initialize session with GET request to SSE endpoint
        print("1. Initializing SSE session...")
        sse_url = "http://127.0.0.1:8000/mcp"  # MCP route is at /mcp
        
        headers = {
            "Accept": "application/json, text/event-stream"
        }
        async with client.stream("GET", sse_url, headers=headers) as response:
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            # Check for CORS headers
            cors_origin = response.headers.get("access-control-allow-origin")
            print(f"   CORS Origin: {cors_origin}")
            
            # Read some initial SSE events
            print("\n2. Reading SSE events (first 5):")
            event_count = 0
            async for line in response.aiter_lines():
                if line:
                    print(f"   Event: {line[:100]}...")
                    event_count += 1
                    if event_count >= 5:
                        break
            
            # Extract session ID from SSE
            session_id = response.headers.get("mcp-session-id")
            print(f"\n3. Session ID: {session_id}")
    
    # Now test a tool call with the session
    if session_id:
        print("\n4. Testing tool call with multi-step task...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Make a tool call that should produce intermediate outputs
            tool_call = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "claude_execute",
                    "arguments": {
                        "prompt": "List the files in the current directory, then create a test.txt file with 'Hello World', then read it back",
                        "working_dir": "/home/rishabh/Desktop/dev/claude-code-mcp"
                    }
                },
                "id": 1
            }
            
            response = await client.post(
                sse_url,
                json=tool_call,
                headers={"Mcp-Session-Id": session_id}
            )
            
            print(f"   Response Status: {response.status_code}")
            print(f"   Response: {response.text[:500]}...")

if __name__ == "__main__":
    print("Testing MCP Server Streaming Capabilities")
    print("==========================================\n")
    asyncio.run(test_mcp_streaming())