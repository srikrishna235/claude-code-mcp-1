#!/usr/bin/env python3
"""Test Claude Code MCP server with file operations"""

import asyncio
import httpx
import json

async def test_file_operation():
    url = "http://127.0.0.1:8000/mcp"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Initialize session
        print("Initializing session...")
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
                    "clientInfo": {"name": "test", "version": "1.0"}
                }
            }
        )
        
        session_id = init_response.headers.get("mcp-session-id")
        print(f"Session ID: {session_id}\n")
        
        # Send initialized notification
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
        
        # Test 1: Analyze the test file
        print("Test 1: Asking Claude Code to analyze test_file.py")
        print("-" * 50)
        
        response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": session_id
            },
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "claude_execute",
                    "arguments": {
                        "prompt": "Read test_file.py and explain what it does",
                        "working_dir": "/home/rishabh/Desktop/dev/claude-code-mcp",
                        "allowed_tools": "Read"
                    }
                }
            }
        )
        
        # Parse response
        if response.headers.get("content-type") == "text/event-stream":
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and isinstance(content, list):
                            for item in content:
                                if item.get("type") == "text":
                                    print(f"Claude's analysis:\n{item.get('text')}")
        
        print("\n" + "=" * 60)
        
        # Test 2: Add a docstring
        print("\nTest 2: Asking Claude Code to add a docstring")
        print("-" * 50)
        
        response = await client.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": session_id
            },
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "claude_execute",
                    "arguments": {
                        "prompt": "Add a docstring to the calculate_sum function in test_file.py explaining what it does",
                        "working_dir": "/home/rishabh/Desktop/dev/claude-code-mcp",
                        "allowed_tools": "Read,Edit"
                    }
                }
            }
        )
        
        # Parse response
        if response.headers.get("content-type") == "text/event-stream":
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and isinstance(content, list):
                            for item in content:
                                if item.get("type") == "text":
                                    print(f"Claude's response:\n{item.get('text')}")
        
        print("\n" + "=" * 60)
        
        # Test 3: Verify the change
        print("\nTest 3: Verifying the file was modified")
        print("-" * 50)
        
        with open("/home/rishabh/Desktop/dev/claude-code-mcp/test_file.py", "r") as f:
            content = f.read()
            print("Current file content:")
            print(content)

if __name__ == "__main__":
    asyncio.run(test_file_operation())