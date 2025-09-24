#!/usr/bin/env python3
import subprocess
import json
import sys

def test_claude():
    """Test if Claude CLI wrapper works"""
    try:
        # Test simple prompt
        test_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": "What is 2+2? Answer with just the number."
                }
            },
            "id": 1
        }
        
        # Try to call claude_code_mcp_final.py
        result = subprocess.run(
            ["python", "claude_code_mcp_final.py"],
            input=json.dumps(test_request),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ Claude CLI wrapper responds")
            return True
        else:
            print("✗ Claude CLI wrapper failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if test_claude() else 1)
