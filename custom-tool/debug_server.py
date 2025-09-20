#!/usr/bin/env python3
"""
Debug the server structure created by SDK
"""

from claude_code_sdk import tool, create_sdk_mcp_server
from typing import Any
import json


# Create a simple tool
@tool("test_tool", "Test tool description", {"input": str})
async def test_tool(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": f"Test: {args.get('input', 'none')}"}]}


# Create server
test_server = create_sdk_mcp_server(
    name="test-server",
    version="1.0.0",
    tools=[test_tool]
)


print("Server Structure Debug")
print("=" * 50)
print(f"Type: {type(test_server)}")
print(f"Is dict: {isinstance(test_server, dict)}")

if isinstance(test_server, dict):
    print("\nDictionary keys:")
    for key in test_server.keys():
        print(f"  - {key}")
    
    print("\nDictionary contents:")
    print(json.dumps(test_server, indent=2, default=str))
    
print("\nAttributes:")
for attr in dir(test_server):
    if not attr.startswith('_'):
        try:
            value = getattr(test_server, attr)
            print(f"  {attr}: {type(value)} = {str(value)[:100] if value else 'None'}")
        except:
            pass