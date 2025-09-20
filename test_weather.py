#!/usr/bin/env python3
import httpx
import asyncio
import json

async def test_weather():
    async with httpx.AsyncClient() as client:
        # Test get_temperature directly
        url = "http://localhost:8003"
        
        # Initialize session
        response = await client.post(url, json={
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {"clientInfo": {"name": "test"}},
            "id": 1
        })
        print("Initialize:", response.status_code)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        
        # List tools
        response = await client.post(url, json={
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        })
        print("\nTools list:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'tools' in data['result']:
                for tool in data['result']['tools']:
                    print(f"  - {tool.get('name')}: {tool.get('description')}")
        
        # Call get_temperature
        response = await client.post(url, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_temperature",
                "arguments": {"city": "London"}
            },
            "id": 3
        })
        print("\nTemperature result:", response.status_code)
        if response.status_code == 200:
            result = response.json()
            if 'result' in result and 'content' in result['result']:
                for item in result['result']['content']:
                    if item.get('type') == 'text':
                        print(item.get('text'))

asyncio.run(test_weather())
