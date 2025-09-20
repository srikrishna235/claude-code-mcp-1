#!/usr/bin/env python3
"""
Example using ClaudeSDKClient as shown in docs
"""

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
from weather_sdk_tool import weather_server
import asyncio


async def main():
    """
    Use weather tools exactly as shown in documentation
    """
    
    # Configure options with weather MCP server
    options = ClaudeCodeOptions(
        mcp_servers={"weather-tools": weather_server},
        allowed_tools=[
            "mcp__weather-tools__get_weather",
            "mcp__weather-tools__get_forecast"
        ]
    )
    
    print("Weather Tools with ClaudeSDKClient")
    print("=" * 50)
    
    try:
        # Use the client exactly as in docs
        async with ClaudeSDKClient(options=options) as client:
            # Query with simple string
            await client.query("What's the weather in San Francisco?")
            
            # Extract and print response
            print("\nResponse:")
            async for msg in client.receive_response():
                print(msg)
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())