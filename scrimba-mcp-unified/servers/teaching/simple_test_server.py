#!/usr/bin/env python3
"""
Simplified MCP server for testing - no Claude calls
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-test")

@mcp.tool()
async def test_echo(message: str) -> str:
    """Simple echo tool for testing"""
    return f"Echo: {message}"

@mcp.tool()
async def test_math(a: int, b: int) -> str:
    """Simple math tool"""
    return f"Result: {a} + {b} = {a + b}"

if __name__ == "__main__":
    import sys
    
    # Print to stderr so it doesn't interfere with stdio
    print("Simple Test MCP Server Started", file=sys.stderr)
    
    # Run in stdio mode
    mcp.run()