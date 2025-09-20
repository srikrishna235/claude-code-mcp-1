#!/bin/bash

echo "Testing scrimba-visual agent..."
echo "================================"

# Test 1: Basic visualization
echo -e "\nTest 1: Visualize concept"
echo "teach me variables" | claude @scrimba-visual --dangerously-skip-permissions 2>&1 | grep -c "generate_image" && echo "ERROR: Found generate_image call!" || echo "✓ No generate_image calls"

# Test 2: Animation request  
echo -e "\nTest 2: Animation request"
echo "animate how loops work" | claude @scrimba-visual --dangerously-skip-permissions 2>&1 | grep -c "multi-tools" && echo "ERROR: Found multi-tools call!" || echo "✓ No multi-tools calls"

# Test 3: Verify scrimba-visual tools used
echo -e "\nTest 3: Check correct tools used"
echo "show me variables" | claude @scrimba-visual --dangerously-skip-permissions 2>&1 | grep -q "scrimba-visual.*visualize_concept" && echo "✓ Using scrimba-visual tools" || echo "ERROR: Not using scrimba-visual tools"

echo -e "\n================================"
echo "Test complete!"