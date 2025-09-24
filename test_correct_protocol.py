#!/usr/bin/env python3
"""
Test MCP servers with the CORRECT protocol format
"""

import subprocess
import json
import sys

def test_mcp_correct_protocol(server_path, tool_name, args):
    """Test MCP server with correct protocol format"""
    
    proc = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Use CORRECT MCP protocol format (not JSON-RPC)
    request = {
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        },
        "id": 1
    }
    
    try:
        stdout, stderr = proc.communicate(
            input=json.dumps(request) + "\n",
            timeout=10
        )
        
        if stdout:
            for line in stdout.strip().split('\n'):
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "result" in data:
                            return "success", data["result"]
                        elif "error" in data:
                            return "error", data["error"]
                    except:
                        pass
            return "error", f"No valid response: {stdout[:200]}"
        else:
            return "error", f"No output (stderr: {stderr[:200] if stderr else 'none'})"
            
    except Exception as e:
        proc.kill()
        return "error", str(e)

def main():
    print("=" * 70)
    print("TESTING WITH CORRECT MCP PROTOCOL")
    print("=" * 70)
    
    servers = [
        ("Our unified server", "scrimba-mcp-unified/servers/teaching/server_unified.py"),
        ("Weather MCP", "weather_mcp.py"),
    ]
    
    for name, path in servers:
        print(f"\n📌 Testing {name}")
        print("-" * 50)
        
        # Test teach tool
        if "teaching" in path:
            status, result = test_mcp_correct_protocol(
                path, "teach", {"topic": "variables", "step": 1}
            )
        else:
            status, result = test_mcp_correct_protocol(
                path, "get_temperature", {"city": "London", "units": "celsius"}
            )
        
        if status == "success":
            print(f"✅ SUCCESS!")
            print(f"   Result: {str(result)[:200]}...")
        else:
            print(f"❌ FAILED")
            print(f"   Error: {result}")
    
    # Also test with different tools
    print("\n📌 Testing multiple tools on unified server")
    print("-" * 50)
    
    tools = [
        ("teach", {"topic": "arrays", "step": 1}),
        ("give_challenge", {"difficulty": "easy"}),
        ("check_code", {"code": "console.log('test');"}),
        ("show_progress", {}),
    ]
    
    for tool_name, args in tools:
        status, result = test_mcp_correct_protocol(
            "scrimba-mcp-unified/servers/teaching/server_unified.py",
            tool_name, args
        )
        
        if status == "success":
            print(f"  ✅ {tool_name}: Works!")
            print(f"     Preview: {str(result)[:100]}...")
        else:
            print(f"  ❌ {tool_name}: {str(result)[:50]}...")
    
    print("\n" + "=" * 70)
    print("PROTOCOL TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()