#!/usr/bin/env python3
"""Test the frontend flow completely"""

import requests
import json
import time

def test_frontend_flow():
    print("Testing Claude Code Terminal Frontend Flow")
    print("=" * 50)
    
    # 1. Test Terminal Server
    print("\n1. Testing Terminal Server (port 8080)...")
    try:
        r = requests.get("http://127.0.0.1:8080")
        if "Claude Code Terminal" in r.text:
            print("   ✅ Terminal HTML served correctly")
        else:
            print("   ❌ Terminal HTML not found")
    except Exception as e:
        print(f"   ❌ Terminal server error: {e}")
    
    # 2. Test MCP Server Initialization
    print("\n2. Testing MCP Server Initialization...")
    try:
        # Initialize session
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        init_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "claude-code-terminal",
                    "version": "1.0.0"
                }
            }
        }
        
        r = requests.post("http://127.0.0.1:8000/mcp", headers=headers, json=init_data)
        
        # Get session ID
        session_id = r.headers.get("mcp-session-id")
        if session_id:
            print(f"   ✅ Session initialized: {session_id}")
        else:
            print("   ❌ No session ID received")
            return
            
    except Exception as e:
        print(f"   ❌ MCP initialization error: {e}")
        return
    
    # 3. Send initialized notification
    print("\n3. Sending initialized notification...")
    try:
        headers["Mcp-Session-Id"] = session_id
        
        notif_data = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        
        r = requests.post("http://127.0.0.1:8000/mcp", headers=headers, json=notif_data)
        print(f"   ✅ Notification sent (status: {r.status_code})")
        
    except Exception as e:
        print(f"   ❌ Notification error: {e}")
    
    # 4. Test calling Claude Code
    print("\n4. Testing Claude Code execution...")
    try:
        call_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": "What is 10 + 15?",
                    "allowed_tools": "Read"
                }
            }
        }
        
        r = requests.post("http://127.0.0.1:8000/mcp", headers=headers, json=call_data)
        
        # Parse SSE response
        if r.headers.get("content-type") == "text/event-stream":
            lines = r.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and isinstance(content, list):
                            for item in content:
                                if item.get("type") == "text":
                                    result = item.get("text", "").strip()
                                    print(f"   ✅ Claude responded: {result}")
                                    if "25" in result:
                                        print("   ✅ Math calculation correct!")
                                    return
                    elif "error" in data:
                        print(f"   ❌ Error: {data['error']}")
                        return
        
        print(f"   ❌ Unexpected response format")
        
    except Exception as e:
        print(f"   ❌ Claude execution error: {e}")
    
    print("\n" + "=" * 50)
    print("Frontend test complete!")
    print("\nIf all tests passed, the frontend should work at:")
    print("http://127.0.0.1:8080")

if __name__ == "__main__":
    test_frontend_flow()