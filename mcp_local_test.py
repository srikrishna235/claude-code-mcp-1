#!/usr/bin/env python3
"""
MCP stdio proxy for LOCAL testing (connects to localhost:8080)
"""
import sys
import json
import requests

# Connect to LOCAL server for testing
REMOTE_URL = "http://localhost:8080/mcp"

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            if line.strip():
                message = json.loads(line.strip())
                
                # Forward to local server
                response = requests.post(
                    REMOTE_URL,
                    json=message,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    sys.stdout.write(json.dumps(result) + "\n")
                    sys.stdout.flush()
                else:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "error": {
                            "code": -32603,
                            "message": f"Server error: {response.status_code}"
                        }
                    }
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()
                    
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()