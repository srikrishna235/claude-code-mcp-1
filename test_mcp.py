#!/usr/bin/env python3
"""Test script to verify Claude Code MCP server is working"""

import asyncio
import httpx
import json

async def test_mcp_server():
    url = "http://127.0.0.1:8000/mcp"
    
    async with httpx.AsyncClient() as client:
        # 1. Initialize
        print("1. Initializing session...")
        init_response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
        )
        
        # Extract session ID
        session_id = init_response.headers.get("mcp-session-id")
        print(f"   Session ID: {session_id}")
        
        # Parse response
        if init_response.headers.get("content-type") == "text/event-stream":
            # Parse SSE response
            lines = init_response.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    print(f"   Response: {data.get('result', {}).get('serverInfo', {})}")
        else:
            print(f"   Response: {init_response.json()}")
        
        # 2. Send initialized notification
        print("\n2. Sending initialized notification...")
        await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": session_id
            },
            json={
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
        )
        print("   Sent.")
        
        # 3. List tools
        print("\n3. Listing tools...")
        tools_response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": session_id
            },
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/list",
                "params": {}
            }
        )
        
        if tools_response.headers.get("content-type") == "text/event-stream":
            lines = tools_response.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "result" in data:
                        tools = data["result"].get("tools", [])
                        for tool in tools:
                            print(f"   - {tool.get('name')}: {tool.get('description')}")
        
        # 4. Call claude_execute tool
        print("\n4. Testing claude_execute tool...")
        call_response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": session_id
            },
            json={
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "claude_execute",
                    "arguments": {
                        "prompt": "What is 5 + 7?",
                        "allowed_tools": "Read"
                    }
                }
            }
        )
        
        print(f"   Status: {call_response.status_code}")
        
        if call_response.headers.get("content-type") == "text/event-stream":
            lines = call_response.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and isinstance(content, list):
                            for item in content:
                                if item.get("type") == "text":
                                    print(f"   Claude's response: {item.get('text')}")
                    elif "error" in data:
                        print(f"   Error: {data['error']}")
        else:
            print(f"   Response: {call_response.text}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())