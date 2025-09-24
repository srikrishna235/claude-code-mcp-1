#!/usr/bin/env python3
"""
Compare our server with the working weather_mcp.py
"""

import subprocess
import json
import sys

def test_server(server_path, tool_name, arguments):
    """Test any MCP server"""
    
    proc = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
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
        return "error", str(e)

def main():
    print("=" * 70)
    print("COMPARING MCP SERVERS")
    print("=" * 70)
    
    # Test 1: Weather MCP (known working)
    print("\n1️⃣ Testing weather_mcp.py (known working)")
    print("-" * 50)
    status, result = test_server(
        "../weather_mcp.py",
        "get_temperature",
        {"city": "London", "units": "celsius"}
    )
    
    if status == "success":
        print(f"✅ Weather MCP works!")
        print(f"   Result: {str(result)[:200]}")
    else:
        print(f"❌ Weather MCP failed: {result}")
    
    # Test 2: Our unified server
    print("\n2️⃣ Testing server_unified.py (our server)")
    print("-" * 50)
    status, result = test_server(
        "servers/teaching/server_unified.py",
        "teach",
        {"topic": "variables", "step": 1}
    )
    
    if status == "success":
        print(f"✅ Unified server works!")
        print(f"   Result: {str(result)[:200]}")
    else:
        print(f"❌ Unified server failed: {result}")
    
    # Test 3: Try different methods on unified server
    print("\n3️⃣ Testing different tool names on unified server")
    print("-" * 50)
    
    tool_names = ["scrimba_agent", "teach", "give_challenge", "check_code"]
    
    for name in tool_names:
        status, result = test_server(
            "servers/teaching/server_unified.py",
            name,
            {"prompt": "test"} if name == "scrimba_agent" else 
            {"topic": "test"} if name == "teach" else
            {"code": "test"} if name == "check_code" else
            {}
        )
        
        if status == "success":
            print(f"  ✅ {name}: Works - {str(result)[:50]}...")
        else:
            print(f"  ❌ {name}: Failed - {str(result)[:50]}")
    
    print("\n" + "=" * 70)
    print("COMPARISON COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()