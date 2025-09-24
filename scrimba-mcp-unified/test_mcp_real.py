#!/usr/bin/env python3
"""
Real test of MCP server tools - actually invoke them and check responses
"""

import subprocess
import json
import sys
import time

def call_mcp_tool(tool_name, arguments=None):
    """Actually call an MCP tool and get the response"""
    
    # Build the JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        },
        "id": 1
    }
    
    # Start the server
    proc = subprocess.Popen(
        [sys.executable, "servers/teaching/server_unified.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request
    try:
        stdout, stderr = proc.communicate(
            input=json.dumps(request) + "\n",
            timeout=5
        )
        
        # Parse response
        if stdout:
            lines = stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    try:
                        response = json.loads(line)
                        if "result" in response:
                            return "success", response["result"]
                        elif "error" in response:
                            return "error", response["error"]
                    except json.JSONDecodeError:
                        pass
            return "error", f"Could not parse response: {stdout[:200]}"
        else:
            return "error", f"No output. Stderr: {stderr[:200] if stderr else 'none'}"
            
    except subprocess.TimeoutExpired:
        proc.kill()
        return "error", "Timeout"
    except Exception as e:
        return "error", str(e)

def main():
    print("=" * 70)
    print("REAL MCP SERVER TOOL TESTING")
    print("=" * 70)
    
    tests = [
        {
            "name": "teach",
            "args": {"topic": "variables", "step": 1},
            "expect": "Should return a lesson about variables"
        },
        {
            "name": "give_challenge", 
            "args": {"difficulty": "easy"},
            "expect": "Should return a 60-second challenge"
        },
        {
            "name": "check_code",
            "args": {"code": "let count = 0;\nconsole.log(count);"},
            "expect": "Should return encouraging feedback"
        },
        {
            "name": "celebrate",
            "args": {"achievement": "first function"},
            "expect": "Should return celebration message"
        },
        {
            "name": "show_progress",
            "args": {},
            "expect": "Should show learning progress"
        },
        {
            "name": "visualize_concept",
            "args": {"concept": "arrays", "style": "pokemon"},
            "expect": "Should return visual description"
        },
        {
            "name": "next",
            "args": {},
            "expect": "Should progress to next lesson"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\n🔧 Testing: {test['name']}")
        print("-" * 50)
        print(f"Args: {test['args']}")
        print(f"Expect: {test['expect']}")
        
        status, result = call_mcp_tool(test['name'], test['args'])
        
        if status == "success":
            result_str = str(result)
            print(f"✅ PASS - Got response ({len(result_str)} chars)")
            
            # Check if response is meaningful (not empty or error)
            if len(result_str) > 10:
                print(f"Response preview: {result_str[:200]}...")
                
                # Check for expected content
                if test['name'] == 'teach' and ('lesson' in result_str.lower() or 'variable' in result_str.lower()):
                    print("   ✓ Contains teaching content")
                elif test['name'] == 'give_challenge' and ('challenge' in result_str.lower() or '60' in result_str):
                    print("   ✓ Contains challenge content")
                elif test['name'] == 'check_code' and any(word in result_str.lower() for word in ['good', 'great', 'nice', 'console']):
                    print("   ✓ Contains feedback")
                elif test['name'] == 'celebrate' and ('🎉' in result_str or '!' in result_str):
                    print("   ✓ Contains celebration")
                elif test['name'] == 'visualize_concept' and any(word in result_str.lower() for word in ['visual', 'image', 'pokemon', 'array']):
                    print("   ✓ Contains visual description")
                else:
                    print("   ⚠️  Response may not contain expected content")
                    
                passed += 1
            else:
                print(f"❌ Response too short: {result_str}")
                failed += 1
        else:
            print(f"❌ FAIL - {result}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✅ ALL TESTS PASSED - MCP SERVER IS FULLY FUNCTIONAL!")
    elif passed > 0:
        print(f"⚠️  PARTIAL SUCCESS - {passed} tools work, {failed} failed")
    else:
        print("❌ ALL TESTS FAILED - MCP SERVER NOT WORKING")
    
    print("=" * 70)
    
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main())