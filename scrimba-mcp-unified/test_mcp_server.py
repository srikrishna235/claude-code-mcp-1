#!/usr/bin/env python3
"""
Test if MCP server starts correctly
"""

import subprocess
import time
import sys

def test_mcp_server():
    """Test the MCP server startup"""
    
    print("Testing MCP Server Startup")
    print("=" * 40)
    
    # Start the server in a subprocess
    process = subprocess.Popen(
        [sys.executable, "servers/teaching/server_claude.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Give it time to start
    time.sleep(2)
    
    # Check if it's still running
    poll = process.poll()
    
    if poll is None:
        print("✅ Server is running!")
        print("   PID:", process.pid)
        
        # Try to get some output
        try:
            stdout, stderr = process.communicate(timeout=1)
            if stdout:
                print("   Output:", stdout[:200])
            if stderr:
                print("   Stderr:", stderr[:200])
        except subprocess.TimeoutExpired:
            print("   Server is waiting for input (normal for MCP server)")
            
        # Kill the server
        process.kill()
        print("   Server stopped")
        return True
    else:
        print("❌ Server exited with code:", poll)
        stdout, stderr = process.communicate()
        if stdout:
            print("   Output:", stdout[:500])
        if stderr:
            print("   Error:", stderr[:500])
        return False

if __name__ == "__main__":
    success = test_mcp_server()
    print("\nResult:", "✅ PASS" if success else "❌ FAIL")