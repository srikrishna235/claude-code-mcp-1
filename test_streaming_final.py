#!/usr/bin/env python3
"""Test if streaming actually works"""

import httpx
import asyncio
import json
import time

async def test_streaming():
    """Test MCP streaming with proper initialization"""
    
    base_url = "http://127.0.0.1:8001/mcp"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("1. Initializing session...")
        
        # Initialize
        response = await client.post(
            base_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0"}
                }
            }
        )
        
        # Get session ID from headers
        session_id = response.headers.get("mcp-session-id")
        print(f"   Session ID: {session_id}")
        
        if not session_id:
            print("ERROR: No session ID received")
            return
        
        # Send initialized notification
        print("2. Sending initialized notification...")
        await client.post(
            base_url,
            headers={
                "Content-Type": "application/json",
                "Mcp-Session-Id": session_id
            },
            json={
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
        )
        
        # Test streaming
        print("3. Testing streaming - watch for progressive output:")
        print("=" * 50)
        
        start_time = time.time()
        
        # Make streaming request
        async with client.stream(
            "POST",
            base_url,
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
                        "prompt": "Create a file test.txt with 'Hello World' and read it back"
                    }
                }
            }
        ) as response:
            print(f"Response status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print("")
            
            # Read SSE stream
            async for line in response.aiter_lines():
                if line:
                    elapsed = time.time() - start_time
                    
                    if line.startswith("event:"):
                        print(f"[{elapsed:5.2f}s] {line}")
                    elif line.startswith("data:"):
                        try:
                            data = json.loads(line[6:])
                            
                            # Check for notifications (streaming updates)
                            if data.get("method") == "notifications/message":
                                message = data["params"].get("message", "")
                                print(f"[{elapsed:5.2f}s] 📢 NOTIFICATION: {message}")
                            elif data.get("method") == "notifications/progress":
                                progress = data["params"].get("progress", 0)
                                message = data["params"].get("message", "")
                                print(f"[{elapsed:5.2f}s] 📊 PROGRESS: {progress}% - {message}")
                            elif data.get("result"):
                                # Final result
                                content = data["result"].get("content", [])
                                if content and content[0].get("text"):
                                    print(f"[{elapsed:5.2f}s] ✅ FINAL RESULT: {content[0]['text'][:100]}...")
                            else:
                                print(f"[{elapsed:5.2f}s] Data: {str(data)[:100]}...")
                        except:
                            print(f"[{elapsed:5.2f}s] Raw: {line[:100]}")

if __name__ == "__main__":
    print("MCP Streaming Test")
    print("==================\n")
    asyncio.run(test_streaming())
    print("\n✅ Test complete")
    print("\nIf you saw NOTIFICATION or PROGRESS messages BEFORE the final result,")
    print("then streaming is working!")