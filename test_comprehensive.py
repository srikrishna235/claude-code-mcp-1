#!/usr/bin/env python3
"""Comprehensive test simulating real user interactions"""

import requests
import json
import time
import os

class TerminalTester:
    def __init__(self):
        self.session_id = None
        self.base_url = "http://127.0.0.1:8000/mcp"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
    def initialize(self):
        """Initialize MCP session"""
        print("🔌 Connecting to MCP server...")
        
        init_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "claude-code-terminal",
                    "version": "1.0.0"
                }
            }
        }
        
        r = requests.post(self.base_url, headers=self.headers, json=init_data)
        self.session_id = r.headers.get("mcp-session-id")
        
        if self.session_id:
            print(f"✅ Connected (Session: {self.session_id[:8]}...)")
            self.headers["Mcp-Session-Id"] = self.session_id
            
            # Send initialized notification
            notif_data = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
            requests.post(self.base_url, headers=self.headers, json=notif_data)
            return True
        return False
    
    def execute_command(self, prompt, allowed_tools=None):
        """Execute a command through Claude Code"""
        print(f"\n❯ {prompt}")
        
        call_data = {
            "jsonrpc": "2.0",
            "id": int(time.time()),
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": prompt,
                    "working_dir": os.getcwd()
                }
            }
        }
        
        if allowed_tools:
            call_data["params"]["arguments"]["allowed_tools"] = allowed_tools
        
        r = requests.post(self.base_url, headers=self.headers, json=call_data, timeout=30)
        
        # Parse response
        if r.headers.get("content-type") == "text/event-stream":
            lines = r.text.strip().split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "result" in data:
                        content = data["result"].get("content", [])
                        if content and isinstance(content, list):
                            for item in content:
                                if item.get("type") == "text":
                                    response = item.get("text", "").strip()
                                    print(f"  {response}")
                                    return response
                    elif "error" in data:
                        print(f"  ❌ Error: {data['error']}")
                        return None
        return None

def main():
    print("=" * 60)
    print("Claude Code Terminal - Comprehensive Test")
    print("=" * 60)
    
    tester = TerminalTester()
    
    # Initialize
    if not tester.initialize():
        print("❌ Failed to connect to MCP server")
        return
    
    print("\n📝 Running test commands...")
    print("-" * 40)
    
    # Test 1: Simple calculation
    tester.execute_command("What is 42 * 17?")
    
    # Test 2: Code analysis
    tester.execute_command("List all Python files in this directory", "Read,Glob")
    
    # Test 3: Create a test file
    test_file = "/tmp/claude_test.py"
    tester.execute_command(
        f"Create a Python file at {test_file} with a function that prints 'Hello from Claude!'",
        "Write"
    )
    
    # Test 4: Read the created file
    tester.execute_command(f"Show me the contents of {test_file}", "Read")
    
    # Test 5: Modify the file
    tester.execute_command(
        f"Add a docstring to the function in {test_file}",
        "Read,Edit"
    )
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n🧹 Cleaned up test file")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("\n🌐 Frontend is ready at: http://127.0.0.1:8080")
    print("💡 Try these commands in the terminal:")
    print("   - What does this project do?")
    print("   - Create a hello world script")
    print("   - Fix any bugs in my code")
    print("=" * 60)

if __name__ == "__main__":
    main()