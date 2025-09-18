#!/bin/bash
# Test Claude CLI through MCP server

echo "Testing Claude CLI via MCP Server"
echo "================================="

# Get session ID
echo "1. Getting session..."
SESSION_ID=$(curl -s -H "Accept: text/event-stream" http://127.0.0.1:8000/mcp -I | grep -i mcp-session-id | cut -d' ' -f2 | tr -d '\r')
echo "   Session ID: $SESSION_ID"

# Call claude_execute tool
echo "2. Calling claude_execute..."
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "claude_execute",
      "arguments": {
        "prompt": "echo Hello from Claude CLI"
      }
    },
    "id": 1
  }')

echo "   Response:"
echo "$RESPONSE" | head -5

echo ""
echo "✅ Test completed"