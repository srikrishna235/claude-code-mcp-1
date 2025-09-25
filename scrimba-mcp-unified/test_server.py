import json
import subprocess
import sys

# Start the MCP server
process = subprocess.Popen(
    ['python', '-m', 'scrimba_mcp_unified'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Initialize
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "0.1.0",
        "clientInfo": {"name": "test-client", "version": "1.0.0"},
        "capabilities": {}
    }
}

process.stdin.write(json.dumps(init_request) + '\n')
process.stdin.flush()

response = process.stdout.readline()
print("Initialize response:", response[:100])

# List tools
tools_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}

process.stdin.write(json.dumps(tools_request) + '\n')
process.stdin.flush()

response = process.stdout.readline()
if response:
    data = json.loads(response)
    tools = data.get('result', {}).get('tools', [])
    print(f"\nTools available: {len(tools)}")
    for tool in tools:
        print(f"  ✓ {tool['name']}")

process.terminate()
