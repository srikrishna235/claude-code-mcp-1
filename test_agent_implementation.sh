#!/bin/bash

echo "==================================="
echo "Testing Agent Implementation"
echo "==================================="
echo ""
echo "This test demonstrates how Claude naturally decides when to use tools"
echo "and how optional agent modes work."
echo ""

# Test 1: Natural weather query (no agent mode)
echo "Test 1: Natural weather query"
echo "------------------------------"
echo "Query: 'What's the weather in London?'"
echo "Expected: Claude sees weather query, uses get_temperature tool"
echo ""
echo "Command: claude -p 'What's the weather in London?' --output-format json --dangerously-skip-permissions"
echo ""

# Test 2: Complex query without agent mode
echo "Test 2: Complex query (natural)"
echo "--------------------------------"
echo "Query: 'Plan my weekend trip to Paris'"
echo "Expected: Claude might check weather as part of planning"
echo ""
echo "Command: claude -p 'Plan my weekend trip to Paris' --output-format json --dangerously-skip-permissions"
echo ""

# Test 3: With weather expert mode
echo "Test 3: Weather expert mode"
echo "----------------------------"
echo "Query: 'Plan my weekend trip to Paris' (with weather expert prompt)"
echo "Expected: Claude acts as weather expert, focuses on weather aspects"
echo ""
echo 'Command: claude -p "Plan my weekend trip to Paris" --append-system-prompt "You are a weather expert. Focus on weather-related travel advice." --output-format json --dangerously-skip-permissions'
echo ""

# Test 4: Through MCP wrapper (simulated)
echo "Test 4: Through MCP Wrapper"
echo "----------------------------"
echo "This simulates how the terminal would call our MCP wrapper"
echo ""
cat > test_mcp_call.py << 'EOF'
import json
import subprocess

def test_claude_execute(prompt, agent_mode=None):
    """Simulate calling our MCP wrapper's claude_execute tool"""
    
    # Build command like our MCP wrapper does
    cmd = ["claude", "-p", prompt]
    cmd.extend(["--output-format", "json"])
    
    if agent_mode == "weather":
        weather_prompt = "You are a weather expert. Use weather tools to provide detailed analysis with practical advice."
        cmd.extend(["--append-system-prompt", weather_prompt])
    
    cmd.append("--dangerously-skip-permissions")
    
    print(f"Testing: {prompt}")
    print(f"Agent mode: {agent_mode or 'None (natural)'}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 40)

# Test cases
test_claude_execute("What's the temperature in Tokyo?")
test_claude_execute("Compare weather in London, Paris, Rome", agent_mode="weather")
EOF

echo "Python simulation of MCP wrapper calls:"
python3 test_mcp_call.py

echo ""
echo "==================================="
echo "Key Points:"
echo "==================================="
echo "1. Without agent_mode: Claude naturally uses tools when appropriate"
echo "2. With agent_mode='weather': Claude acts as weather expert"
echo "3. The terminal doesn't need to detect - just passes user query"
echo "4. Claude's intelligence decides the best approach"