#!/usr/bin/env python3
"""
Fixed MCP stdio proxy for remote Render server
Bridges Claude Code's stdio transport with the remote HTTP server
"""

import sys
import json
import asyncio
import httpx
from typing import Dict, Any

REMOTE_URL = "https://claude-code-mcp-1.onrender.com/mcp"

async def call_remote(method: str, params: Dict = None) -> Dict:
    """Call remote MCP server"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        request_data = {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1,
            "params": params or {}
        }
        
        response = await client.post(
            REMOTE_URL,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {"code": -32603, "message": f"Remote error: {response.status_code}"}
            }

async def main():
    """Main stdio loop"""
    # Process stdin/stdout line by line
    for line in sys.stdin:
        try:
            if not line.strip():
                continue
                
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            # Call remote server
            if method == "initialize":
                remote_response = await call_remote("initialize", params)
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": remote_response.get("result", {})
                }
            elif method == "tools/list":
                remote_response = await call_remote("tools/list", params)
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": remote_response.get("result", {})
                }
            elif method == "tools/call":
                remote_response = await call_remote("tools/call", params)
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": remote_response.get("result", {})
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
            
            # Send response
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())