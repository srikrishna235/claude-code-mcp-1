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