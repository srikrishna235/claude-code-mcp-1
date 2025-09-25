#!/usr/bin/env python3
from fastmcp import FastMCP

mcp = FastMCP("simple-test")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello"""
    return f"Hello {name}!"

if __name__ == "__main__":
    mcp.run()
