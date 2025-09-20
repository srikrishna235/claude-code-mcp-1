from claude_code_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeCodeOptions
from typing import Any
import aiohttp

# Define a custom tool using the @tool decorator
@tool("get_weather", "Get current weather for a location", {"location": str, "units": str})
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    # Call weather API
    units = args.get('units', 'celsius')
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.weather.com/v1/current?q={args['location']}&units={units}"
        ) as response:
            data = await response.json()
    
    return {
        "content": [{
            "type": "text",
            "text": f"Temperature: {data['temp']}°\nConditions: {data['conditions']}\nHumidity: {data['humidity']}%"
        }]
    }

# Create an SDK MCP server with the custom tool
custom_server = create_sdk_mcp_server(
    name="my-custom-tools",
    version="1.0.0",
    tools=[get_weather]  # Pass the decorated function
)

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
import asyncio

# Use the custom tools with Claude
options = ClaudeCodeOptions(
    mcp_servers={"my-custom-tools": custom_server},
    allowed_tools=[
        "mcp__my-custom-tools__get_weather",  # Allow the weather tool
        # Add other tools as needed
    ]
)

async def main():
    async with ClaudeSDKClient(options=options) as client:
        await client.query("What's the weather in San Francisco?")
        
        # Extract and print response
        async for msg in client.receive_response():
            print(msg)

asyncio.run(main())