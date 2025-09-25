#!/usr/bin/env python3
"""
MCP stdio proxy that connects to remote Render server
"""
import sys
import json
import requests

REMOTE_URL = "https://claude-code-mcp-1.onrender.com/mcp"

# Process stdin line by line
for line in sys.stdin:
    try:
        request = json.loads(line.strip())
        
        # Forward to remote server
        response = requests.post(REMOTE_URL, json=request, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result))
            sys.stdout.flush()
        else:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32603, "message": f"Remote error: {response.status_code}"}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
            
    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": request.get("id") if 'request' in locals() else None,
            "error": {"code": -32603, "message": str(e)}
        }
        print(json.dumps(error_response))
        sys.stdout.flush()