#!/usr/bin/env python3
"""
Test the unified MCP server
"""

import subprocess
import json
import sys
import time

def test_tool(tool_name, arguments):
    """Test a single tool in STDIO mode"""
    
    # Create JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }
    
    # Start server
    proc = subprocess.Popen(
        [sys.executable, "servers/teaching/server_unified.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request and get response
    try:
        stdout, stderr = proc.communicate(
            input=json.dumps(request) + "\n",
            timeout=10
        )
        
        # Parse response
        if stdout:
            for line in stdout.strip().split('\n'):
                if line.strip():
                    try:
                        response = json.loads(line)
                        if "result" in response:
                            return True, response["result"]
                        elif "error" in response:
                            return False, f"Error: {response['error']}"
                    except json.JSONDecodeError:
                        pass
            return False, f"Invalid response: {stdout[:200]}"
        else:
            return False, f"No output (stderr: {stderr[:200]})"
            
    except subprocess.TimeoutExpired:
        proc.kill()
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    """Run comprehensive tests"""
    print("=" * 60)
    print("TESTING UNIFIED MCP SERVER")
    print("=" * 60)
    
    tests = [
        ("teach", {"topic": "variables", "step": 1}),
        ("give_challenge", {"difficulty": "easy"}),
        ("check_code", {"code": "let myName = 'Test';\nconsole.log(myName);"}),
        ("next", {}),
        ("celebrate", {"achievement": "first variable"}),
        ("show_progress", {}),
        ("visualize_concept", {"concept": "arrays"}),
        ("variable_visualizer", {"name": "count", "value": "5"})
    ]
    
    passed = 0
    failed = 0
    
    for tool_name, args in tests:
        print(f"\n📌 Testing: {tool_name}")
        print("-" * 40)
        
        success, result = test_tool(tool_name, args)
        
        if success:
            print("✅ PASS")
            print(f"   Result preview: {str(result)[:150]}...")
            passed += 1
        else:
            print("❌ FAIL")
            print(f"   Error: {result}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())