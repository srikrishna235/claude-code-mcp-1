#!/bin/bash

echo "==================================================="
echo "TESTING COMPLETE SCRIMBA FLOW"
echo "==================================================="

echo -e "\n1️⃣ TEST: Teaching Variables"
echo "teach me variables" | claude @scrimba-teacher --dangerously-skip-permissions 2>&1 | head -30

echo -e "\n==================================================="
echo "2️⃣ TEST: Code Without console.log"
echo "let myAge = 25" | claude @scrimba-teacher --dangerously-skip-permissions 2>&1 | grep -A5 "console.log" | head -10

echo -e "\n==================================================="
echo "3️⃣ TEST: Error Learning"
echo "why doesn't console.log(x) work" | claude @scrimba-teacher --dangerously-skip-permissions 2>&1 | grep -A5 "Error" | head -10

echo -e "\n==================================================="
echo "4️⃣ TEST: Visual Teaching"
echo "visualize variables" | claude @agent-orchestrator --dangerously-skip-permissions 2>&1 | head -20

echo -e "\n==================================================="
echo "✅ ALL TESTS COMPLETE"
echo "==================================================="

# Verify tools are registered
echo -e "\n📋 CHECKING AVAILABLE TOOLS:"
python -c "
from scrimba_mcp import mcp
import asyncio

async def check():
    tools = await mcp.list_tools()
    print(f'Total tools available: {len(tools)}')
    new_tools = ['console_log_check', 'learn_by_breaking', 'progressive_challenge']
    for tool in new_tools:
        found = any(t.name == tool for t in tools)
        print(f'  ✓ {tool}: {'Found' if found else 'Missing'}')

asyncio.run(check())
" 2>&1