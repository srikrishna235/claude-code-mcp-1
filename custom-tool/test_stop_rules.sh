#!/bin/bash

echo "================================="
echo "TESTING STOP RULES - NO CASCADING"
echo "================================="

echo -e "\n🧪 TEST 1: scrimba-visual (should call ONE tool only)"
echo "Request: 'visualize variables'"
echo "Expected: ONE visualize_concept call, NO generate_image"
echo "---"
timeout 5 bash -c 'echo "visualize variables" | claude @scrimba-visual --dangerously-skip-permissions 2>&1 | grep -c "generate_image"' || true
echo "generate_image calls: $(echo "visualize variables" | timeout 5 claude @scrimba-visual --dangerously-skip-permissions 2>&1 | grep -c "generate_image" || echo "0")"
echo "✅ Should be 0"

echo -e "\n🧪 TEST 2: visual-teacher (should return prompt, not generate)"  
echo "Request: 'let pikachu = 3'"
echo "Expected: ONE variable_visualizer call, NO image generation"
echo "---"
timeout 5 bash -c 'echo "let pikachu = 3" | claude @visual-teacher --dangerously-skip-permissions 2>&1 | head -20'

echo -e "\n🧪 TEST 3: Count tool calls"
echo "Request: 'teach me variables'"
echo "Expected: 1-2 tool calls max (lesson + challenge)"
echo "---"
echo "teach me variables" | timeout 10 claude @scrimba-teacher --dangerously-skip-permissions 2>&1 | grep -c "mcp__" || echo "Tool calls: 0"

echo -e "\n================================="
echo "✅ TESTS COMPLETE"
echo "Success = No infinite loops, no generate_image calls"
echo "================================="