#!/usr/bin/env python3
"""Test MCP server with claude_execute"""

import httpx
import json
import asyncio

async def test():
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Get session
        print("1. Getting session...")
        headers = {"Accept": "text/event-stream"}
        response = await client.get("http://127.0.0.1:8000/mcp", headers=headers)
        session_id = response.headers.get("mcp-session-id")
        print(f"   Session ID: {session_id}")
        
        # 2. Initialize session
        print("2. Initializing session...")
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
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
            json=init_request,
            headers=headers
        )
        print(f"   Init: {response.status_code}")
        
        # 2.5. Send initialized notification
        print("2.5. Sending initialized notification...")
        init_notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        response = await client.post(
            "http://127.0.0.1:8000/mcp",
            json=init_notif,
            headers=headers
        )
        print(f"   Initialized: {response.status_code}")
        
        # 3. Call claude_execute
        print("3. Calling claude_execute...")
        tool_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": "Create a Python file called server_test.py that prints 'MCP Server Test', calculates 10 * 3, prints the result, then execute the file"
                }
            },
            "id": 2
        }
        
        response = await client.post(
            "http://127.0.0.1:8000/mcp",
            json=tool_request,
            headers=headers
        )
        
        print(f"   Response: {response.text}")

if __name__ == "__main__":
    asyncio.run(test())
    
    # Check if file was created
    import os
    if os.path.exists("server_test.py"):
        print("\n✅ File created successfully")
        print("Contents:")
        with open("server_test.py") as f:
            print(f.read())