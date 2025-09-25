from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool()
async def hello(name: str) -> str:
    """Say hello"""
    return f"Hello {name}!"

# Check if tool is registered
print(f"Tools registered: {len(mcp._tool_manager._tools)}")
for tool_name in mcp._tool_manager._tools:
    print(f"  - {tool_name}")
