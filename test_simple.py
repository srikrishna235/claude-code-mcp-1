#!/usr/bin/env python3
"""Simple test to verify MCP server is working with intermediate outputs"""

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import StreamableHTTPTransport

async def test_claude_execute():
    """Test the claude_execute tool with a multi-step task"""
    
    # Create transport and session
    transport = StreamableHTTPTransport(url="http://127.0.0.1:8000/mcp")
    
    async with ClientSession(transport) as session:
        # Initialize the session
        await session.initialize()
        
        print("Session initialized successfully!")
        print(f"Available tools: {[tool.name for tool in session.tools]}")
        
        # Call the claude_execute tool with a multi-step task
        result = await session.call_tool(
            "claude_execute",
            {
                "prompt": "First, list the files in the current directory. Then create a file called test_output.txt with the content 'Intermediate outputs are working!'. Finally, read the file back to verify it was created.",
                "working_dir": "/home/rishabh/Desktop/dev/claude-code-mcp"
            }
        )
        
        print("\nTool execution result:")
        print(result)
        
        return result

if __name__ == "__main__":
    print("Testing MCP Server - Intermediate Outputs")
    print("=========================================\n")
    
    try:
        result = asyncio.run(test_claude_execute())
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")