#!/bin/bash
# Start MCP servers and test with proper permissions

echo "Starting Scrimba Teaching MCP Server..."
python teaching-server/teaching_mcp.py &
SERVER_PID=$!
sleep 2

echo "Testing with allowed tools..."
echo

# Test 1: With explicit tool permissions
echo "Test 1: Teach with allowed tools"
claude "teach me variables" \
  --allowedTools "mcp__scrimba-teaching__teach" \
  --dangerously-skip-permissions

# Test 2: Allow all scrimba-teaching tools
echo "Test 2: Challenge with wildcard permissions"
claude "give me a coding challenge" \
  --allowedTools "mcp__scrimba-teaching__*" \
  --dangerously-skip-permissions

# Test 3: Check available MCP tools
echo "Test 3: List available MCP tools"
claude "what MCP tools are available?" \
  --dangerously-skip-permissions

kill $SERVER_PID