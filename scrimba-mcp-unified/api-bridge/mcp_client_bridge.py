#!/usr/bin/env python3
"""
MCP Client Bridge using Official SDK
Proper implementation using mcp.client.stdio
"""

import asyncio
import os
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClientBridge:
    """MCP Client that connects to our teaching server via stdio"""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        
    async def connect(self):
        """Connect to the Scrimba Teaching MCP server"""
        # Server parameters - exactly like Claude Code config
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "scrimba_teaching_mcp"]
        )
        
        # Connect to the server using stdio
        read, write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        
        # Create and initialize session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        
        # Initialize the connection
        result = await self.session.initialize()
        print(f"Connected to MCP server: {result.serverInfo.name}")
        
        return self
        
    async def list_tools(self):
        """List available tools from the server"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
            
        result = await self.session.list_tools()
        return [tool.name for tool in result.tools]
        
    async def call_tool(self, name: str, arguments: dict = None):
        """Call a tool on the server"""
        if not self.session:
            raise RuntimeError("Not connected. Call connect() first.")
            
        result = await self.session.call_tool(name, arguments=arguments or {})
        
        # Extract content from the result
        if hasattr(result, 'content') and len(result.content) > 0:
            # Get the text content
            content_item = result.content[0]
            if hasattr(content_item, 'text'):
                return content_item.text
            return str(content_item)
        return result
        
    async def close(self):
        """Close the connection"""
        await self.exit_stack.aclose()
        
    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, *exc):
        await self.close()


async def test_mcp_client():
    """Test the MCP client bridge"""
    async with MCPClientBridge() as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Test teaching
        result = await client.call_tool("teach", {"topic": "variables", "step": 1})
        print(f"\nTeach result: {result[:200]}...")
        
        # Test challenge
        result = await client.call_tool("give_challenge", {"difficulty": "easy"})
        print(f"\nChallenge result: {result[:200]}...")
        
        # Test code checking
        result = await client.call_tool("check_code", {"code": "let x = 5"})
        print(f"\nCheck result: {result}")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_mcp_client())