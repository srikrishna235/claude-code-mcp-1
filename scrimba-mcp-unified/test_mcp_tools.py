#!/usr/bin/env python3
"""
Test MCP server tools with real inputs
"""

import subprocess
import requests
import json
import time
import sys

def start_server():
    """Start MCP server in HTTP mode"""
    print("Starting MCP server in HTTP mode...")
    process = subprocess.Popen(
        [sys.executable, "servers/teaching/server_claude.py", "--http"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(5)
    
    # Check if running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print("❌ Server failed to start!")
        print("stdout:", stdout)
        print("stderr:", stderr)
        return None
    
    print("✅ Server started with PID:", process.pid)
    return process

def test_tool(tool_name, arguments):
    """Test a specific MCP tool"""
    url = "http://localhost:8007/tools/call"
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }
    
    try:
        response = requests.post(url, json=payload, timeout=35)
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                return True, data["result"]
            elif "error" in data:
                return False, data["error"]
            else:
                return False, "No result in response"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout (>35s)"
    except Exception as e:
        return False, str(e)

def run_tests():
    """Run comprehensive tests"""
    print("\n" + "=" * 60)
    print("MCP SERVER COMPREHENSIVE TEST")
    print("=" * 60)
    
    # Start server
    server = start_server()
    if not server:
        return False
    
    all_passed = True
    
    try:
        # Test 1: teach_concept
        print("\n📚 Test 1: teach_concept")
        print("-" * 40)
        success, result = test_tool("teach_concept", {"topic": "variables", "step": 1})
        if success:
            print("✅ PASS - Got response")
            print("   Response preview:", str(result)[:200] + "...")
            # Check if it's actually from Claude (not fallback)
            if "60 seconds" in str(result) or "Type THIS" in str(result):
                print("   ✅ Contains Scrimba elements")
            else:
                print("   ⚠️  May be fallback response")
        else:
            print("❌ FAIL -", result)
            all_passed = False
        
        # Test 2: give_challenge
        print("\n⚡ Test 2: give_challenge")
        print("-" * 40)
        success, result = test_tool("give_challenge", {"difficulty": "easy"})
        if success:
            print("✅ PASS - Got response")
            print("   Response preview:", str(result)[:200] + "...")
            if "60-SECOND" in str(result) or "CHALLENGE" in str(result):
                print("   ✅ Contains challenge format")
            else:
                print("   ⚠️  May be fallback response")
        else:
            print("❌ FAIL -", result)
            all_passed = False
        
        # Test 3: check_code
        print("\n✔️ Test 3: check_code")
        print("-" * 40)
        test_code = "let myName = 'Test';\nconsole.log(myName);"
        success, result = test_tool("check_code", {"code": test_code})
        if success:
            print("✅ PASS - Got response")
            print("   Response preview:", str(result)[:200] + "...")
            if "console.log" in str(result) or "great" in str(result).lower():
                print("   ✅ Acknowledged console.log usage")
            else:
                print("   ⚠️  May be generic response")
        else:
            print("❌ FAIL -", result)
            all_passed = False
        
        # Test 4: next_lesson
        print("\n➡️ Test 4: next_lesson")
        print("-" * 40)
        success, result = test_tool("next_lesson", {})
        if success:
            print("✅ PASS - Got response")
            print("   Response preview:", str(result)[:200] + "...")
        else:
            print("❌ FAIL -", result)
            all_passed = False
        
        # Test 5: celebrate
        print("\n🎉 Test 5: celebrate")
        print("-" * 40)
        success, result = test_tool("celebrate", {"achievement": "first variable"})
        if success:
            print("✅ PASS - Got response")
            print("   Response preview:", str(result)[:200] + "...")
            if "🎉" in str(result) or "!" in str(result):
                print("   ✅ Contains celebration elements")
        else:
            print("❌ FAIL -", result)
            all_passed = False
        
        # Test 6: show_hint
        print("\n💡 Test 6: show_hint")
        print("-" * 40)
        success, result = test_tool("show_hint", {"level": 1})
        if success:
            print("✅ PASS - Got response")
            print("   Response preview:", str(result)[:200] + "...")
        else:
            print("❌ FAIL -", result)
            all_passed = False
        
    finally:
        # Kill server
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ ALL TESTS PASSED!")
        else:
            print("❌ SOME TESTS FAILED")
        print("=" * 60)
        
        print("\nStopping server...")
        server.terminate()
        server.wait(timeout=5)
        print("Server stopped")
    
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)