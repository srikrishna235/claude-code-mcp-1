#!/usr/bin/env python3
"""
Local MCP proxy for remote Render deployment
This bridges Claude Code's stdio transport with the remote HTTP server
"""

import sys
import json
import asyncio
import httpx
from typing import Dict, Any

REMOTE_URL = "https://claude-code-mcp-1.onrender.com/mcp"
API_KEY = "scrimba-teaching-secure-key-2024"

async def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Forward request to remote MCP server"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                REMOTE_URL,
                json={"prompt": request.get("params", {}).get("prompt", ""), "mode": "auto"},
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": API_KEY
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": data.get("result", {})
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32603, "message": f"Remote server error: {response.status_code}"}
                }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32603, "message": str(e)}
            }

async def main():
    """Main stdio loop for MCP protocol"""
    # Read and process requests
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            
            # Handle different request types
            if request.get("method") == "initialize":
                # Handle initialization
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "1.0.0",
                        "serverInfo": {
                            "name": "scrimba-remote-proxy",
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }
            elif request.get("method") == "tools/list":
                # Return available tools
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "scrimba_teach",
                                "description": "Teach programming concepts",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "prompt": {"type": "string"}
                                    }
                                }
                            }
                        ]
                    }
                }
            elif request.get("method") == "tools/call":
                # Forward to remote server
                response = await handle_request(request)
            else:
                # Unknown method
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())