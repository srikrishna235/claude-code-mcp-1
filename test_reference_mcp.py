#!/usr/bin/env python3
"""
Test the reference MCP implementation to understand the protocol
"""

import subprocess
import json
import sys
import os

def test_mcp_server(server_cmd, tool_name, args):
    """Test any MCP server with raw JSON-RPC"""
    
    proc = subprocess.Popen(
        server_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(server_cmd[1]) if len(server_cmd) > 1 else None
    )
    
    # Try direct tool call (what we've been doing)
    request = {
        "jsonrpc": "2.0",
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
            timeout=5
        )
        
        print(f"STDOUT: {stdout[:500] if stdout else 'none'}")
        print(f"STDERR: {stderr[:200] if stderr else 'none'}")
        
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
        return "error", "No valid response"
    except Exception as e:
        proc.kill()
        return "error", str(e)

def test_with_claude_code():
    """Test how Claude Code actually invokes MCP servers"""
    
    # Claude Code uses --dangerously-skip-permissions
    import subprocess
    
    # Create a test prompt that would use MCP tools
    prompt = "Use the teach tool to teach me about variables"
    
    # Try to invoke via Claude Code CLI
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--dangerously-skip-permissions"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("Claude Code response:")
        print(result.stdout[:1000] if result.stdout else "No output")
        
        if result.returncode != 0:
            print(f"Error: {result.stderr[:500]}")
            
    except Exception as e:
        print(f"Could not test with Claude Code: {e}")

def main():
    print("=" * 70)
    print("TESTING MCP PROTOCOL")
    print("=" * 70)
    
    # Test 1: Reference implementation
    print("\n1. Testing reference implementation")
    print("-" * 40)
    status, result = test_mcp_server(
        [sys.executable, "-m", "scrimba_teaching_mcp"],
        "teach",
        {"topic": "variables", "step": 1}
    )
    print(f"Result: {status}")
    if status == "error":
        print(f"Error details: {result}")
    else:
        print(f"Success: {str(result)[:200]}")
    
    # Test 2: Our implementation  
    print("\n2. Testing our implementation")
    print("-" * 40)
    status, result = test_mcp_server(
        [sys.executable, "scrimba-mcp-unified/servers/teaching/server_unified.py"],
        "teach",
        {"topic": "variables", "step": 1}
    )
    print(f"Result: {status}")
    if status == "error":
        print(f"Error details: {result}")
    else:
        print(f"Success: {str(result)[:200]}")
    
    # Test 3: Try Claude Code
    print("\n3. Testing with Claude Code CLI")
    print("-" * 40)
    test_with_claude_code()
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()