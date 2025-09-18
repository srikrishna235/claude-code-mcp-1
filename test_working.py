#!/usr/bin/env python3
"""Working test of Claude CLI through MCP server"""

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
        
        print(f"   Init response: {response.status_code}")
        
        # 2.5. List available tools
        print("2.5. Listing available tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 2
        }
        
        response = await client.post(
            "http://127.0.0.1:8000/mcp",
            json=list_tools_request,
            headers=headers
        )
        
        print(f"   Tools response: {response.text[:500]}")
        
        # 3. Call claude_execute
        print("3. Calling claude_execute...")
        tool_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": "Create a file mcp_test.txt with 'MCP is working!' and read it back"
                }
            },
            "id": 2
        }
        
        response = await client.post(
            "http://127.0.0.1:8000/mcp",
            json=tool_request,
            headers=headers
        )
        
        print(f"   Tool response status: {response.status_code}")
        print(f"   Response (first 200 chars): {response.text[:200]}")

if __name__ == "__main__":
    print("Testing Claude CLI through MCP Server")
    print("======================================\n")
    asyncio.run(test())
    print("\n✅ Test completed")