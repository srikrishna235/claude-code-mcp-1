import json
import subprocess
import sys

# Start server
process = subprocess.Popen(
    ['scrimba-mcp-unified'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Initialize
init = {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0","clientInfo":{"name":"test","version":"1.0"},"capabilities":{}}}
process.stdin.write(json.dumps(init) + '\n')
process.stdin.flush()

init_resp = process.stdout.readline()
print("Initialize:", "✓" if "result" in init_resp else "✗")

# List tools  
tools_req = {"jsonrpc":"2.0","id":2,"method":"tools/list"}
process.stdin.write(json.dumps(tools_req) + '\n')
process.stdin.flush()

tools_resp = process.stdout.readline()
data = json.loads(tools_resp)
tools = data.get('result', {}).get('tools', [])
print(f"\nTools available: {len(tools)}")
for tool in tools:
    print(f"  ✓ {tool['name']}")

# Test a tool call if tools exist
if tools:
    call_req = {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"teach","arguments":{"topic":"variables","step":1}}}
    process.stdin.write(json.dumps(call_req) + '\n')
    process.stdin.flush()
    
    call_resp = process.stdout.readline()
    if "result" in call_resp:
        result = json.loads(call_resp)
        content = result.get('result', {}).get('content', [])
        if content:
            text = content[0].get('text', '')[:100]
            print(f"\nTool call worked: {text[:50]}...")

process.terminate()
