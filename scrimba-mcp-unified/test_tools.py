import json
import subprocess

# Start server
process = subprocess.Popen(
    ['scrimba-mcp-unified'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Initialize
init_req = {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0","clientInfo":{"name":"test","version":"1.0"},"capabilities":{}}}
process.stdin.write(json.dumps(init_req) + '\n')
process.stdin.flush()
response = process.stdout.readline()
print("Initialize:", "✓" if "result" in response else "✗")

# List tools
tools_req = {"jsonrpc":"2.0","id":2,"method":"tools/list"}
process.stdin.write(json.dumps(tools_req) + '\n')
process.stdin.flush()
response = process.stdout.readline()
data = json.loads(response)
tools = data.get('result', {}).get('tools', [])
print(f"Tools found: {len(tools)}")
for tool in tools:
    print(f"  ✓ {tool['name']}")

# Test a tool
if tools:
    call_req = {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"teach","arguments":{"topic":"variables","step":1}}}
    process.stdin.write(json.dumps(call_req) + '\n')
    process.stdin.flush()
    response = process.stdout.readline()
    if "result" in response:
        print("Tool call: ✓ Working")

process.terminate()
