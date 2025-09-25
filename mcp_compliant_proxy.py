#!/usr/bin/env python3
"""
Fully MCP-compliant stdio proxy for remote Render server
"""
import sys
import json
import requests
import threading
import time

REMOTE_URL = "https://claude-code-mcp-1.onrender.com/mcp"

def read_stdin():
    """Read JSON-RPC messages from stdin"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            if line.strip():
                message = json.loads(line.strip())
                
                # Forward to remote server
                try:
                    response = requests.post(
                        REMOTE_URL,
                        json=message,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Ensure we have proper JSON-RPC response
                        if "jsonrpc" not in result:
                            result["jsonrpc"] = "2.0"
                        if "id" not in result and "id" in message:
                            result["id"] = message["id"]
                        
                        sys.stdout.write(json.dumps(result) + "\n")
                        sys.stdout.flush()
                    else:
                        error_response = {
                            "jsonrpc": "2.0",
                            "id": message.get("id"),
                            "error": {
                                "code": -32603,
                                "message": f"Remote server error: {response.status_code}"
                            }
                        }
                        sys.stdout.write(json.dumps(error_response) + "\n")
                        sys.stdout.flush()
                        
                except requests.exceptions.RequestException as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "error": {
                            "code": -32603,
                            "message": f"Connection error: {str(e)}"
                        }
                    }
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()
                    
        except json.JSONDecodeError:
            # Invalid JSON, skip
            continue
        except Exception as e:
            # Log error but continue
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    # Start reading stdin
    read_stdin()