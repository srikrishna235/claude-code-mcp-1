#!/usr/bin/env python3
"""
Verify both old and new MCP servers are working
"""

import subprocess
import json
import time

def test_server(command, args):
    """Test if a server starts successfully."""
    try:
        # Start server and wait briefly
        process = subprocess.Popen(
            ["python"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        time.sleep(0.5)
        
        # Check if still running
        if process.poll() is None:
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"  Error: {stderr[:200]}")
            return False
    except Exception as e:
        print(f"  Exception: {e}")
        return False

def main():
    print("=" * 60)
    print("DUAL SERVER VERIFICATION")
    print("=" * 60)
    
    # Load config
    with open("/home/rishabh/Desktop/dev/claude-code-mcp/.mcp.json", "r") as f:
        config = json.load(f)
    
    servers = config["mcpServers"]
    
    print("\n📦 ORIGINAL SERVERS (custom-tool/):")
    print("-" * 40)
    original = ["scrimba-tools", "scrimba-visual", "visual-code", "scrimba-teaching"]
    for name in original:
        if name in servers:
            args = servers[name]["args"]
            status = "✅" if test_server("python", args) else "❌"
            print(f"{status} {name}: {' '.join(args)}")
    
    print("\n🔧 NEW MODULAR SERVERS (servers/):")
    print("-" * 40)
    v2_servers = ["scrimba-teaching-v2", "scrimba-visual-v2", "scrimba-visual-code-v2", "scrimba-projects-v2"]
    for name in v2_servers:
        if name in servers:
            args = servers[name]["args"]
            status = "✅" if test_server("python", args) else "❌"
            print(f"{status} {name}: {' '.join(args)}")
    
    print("\n" + "=" * 60)
    print("✨ RECOMMENDATION:")
    print("Both server sets are configured! You can:")
    print("1. Use original servers for stability")
    print("2. Use v2 servers for new modular features")
    print("3. Gradually migrate from original to v2")
    print("=" * 60)

if __name__ == "__main__":
    main()