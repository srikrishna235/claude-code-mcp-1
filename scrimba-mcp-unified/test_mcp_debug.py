#!/usr/bin/env python3
"""
Debug MCP server to find out why tools aren't working
"""

import subprocess
import json
import sys

def test_mcp_protocol():
    """Test the MCP protocol with proper initialization"""
    
    # Start the server
    proc = subprocess.Popen(
        [sys.executable, "servers/teaching/server_unified.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Test different request formats
    requests = [
        {
            "name": "Initialize",
            "request": {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "1.0.0",
                    "capabilities": {}
                },
                "id": 0
            }
        },
        {
            "name": "List Tools",
            "request": {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 1
            }
        },
        {
            "name": "Call teach (with correct name)",
            "request": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "teach",
                    "arguments": {"topic": "variables", "step": 1}
                },
                "id": 2
            }
        },
        {
            "name": "Call teach (alternative format)",
            "request": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "tool": "teach",
                    "args": {"topic": "variables", "step": 1}
                },
                "id": 3
            }
        }
    ]
    
    print("=" * 70)
    print("MCP PROTOCOL DEBUG TEST")
    print("=" * 70)
    
    # Send all requests
    all_requests = "\n".join(json.dumps(r["request"]) for r in requests) + "\n"
    
    try:
        stdout, stderr = proc.communicate(input=all_requests, timeout=10)
        
        print("\n📥 STDOUT Response:")
        print("-" * 50)
        if stdout:
            # Try to parse each line as JSON
            for i, line in enumerate(stdout.strip().split('\n')):
                if line.strip():
                    print(f"\nLine {i+1}: {line[:200]}")
                    try:
                        data = json.loads(line)
                        if "error" in data:
                            print(f"  ❌ Error: {data['error']}")
                        elif "result" in data:
                            result = data.get('result', {})
                            if isinstance(result, dict):
                                if 'tools' in result:
                                    print(f"  ✅ Tools found: {len(result['tools'])} tools")
                                    for tool in result['tools'][:3]:
                                        print(f"     - {tool.get('name', 'unnamed')}")
                                else:
                                    print(f"  ✅ Result: {str(result)[:100]}")
                            else:
                                print(f"  ✅ Result: {str(result)[:100]}")
                    except json.JSONDecodeError:
                        print(f"  ⚠️  Not valid JSON")
        else:
            print("No stdout output")
        
        print("\n📤 STDERR Output:")
        print("-" * 50)
        if stderr:
            print(stderr[:500])
        else:
            print("No stderr output")
            
    except subprocess.TimeoutExpired:
        proc.kill()
        print("❌ Process timed out")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("DEBUG COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_mcp_protocol()