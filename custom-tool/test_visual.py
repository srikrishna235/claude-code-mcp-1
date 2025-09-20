#!/usr/bin/env python3
"""Test the visual MCP tools"""

import asyncio
import sys
sys.path.append('/home/rishabh/Desktop/dev/claude-code-mcp/custom-tool')

from scrimba_visual_mcp import (
    visualize_concept,
    animate_concept,
    visual_challenge,
    explain_with_diagram,
    create_meme
)

async def test_visual_tools():
    print("Testing Visual MCP Tools\n" + "="*50)
    
    # Test 1: Visualize concept
    print("\n1. VISUALIZE CONCEPT - Variables")
    result = await visualize_concept("variables")
    print(result[:500] + "...\n")
    
    # Test 2: Animate concept
    print("\n2. ANIMATE CONCEPT - Loops")
    result = await animate_concept("loops", 3)
    print(result[:500] + "...\n")
    
    # Test 3: Visual challenge
    print("\n3. VISUAL CHALLENGE")
    result = await visual_challenge("easy")
    print(result[:500] + "...\n")
    
    # Test 4: Explain code with diagram
    print("\n4. EXPLAIN CODE WITH DIAGRAM")
    code = "for(let i = 0; i < 5; i++) { console.log(i); }"
    result = await explain_with_diagram(code)
    print(result[:500] + "...\n")
    
    # Test 5: Create meme
    print("\n5. CREATE PROGRAMMING MEME")
    result = await create_meme("debugging", "relatable")
    print(result[:500] + "...\n")
    
    print("="*50)
    print("All visual tools tested successfully!")

if __name__ == "__main__":
    asyncio.run(test_visual_tools())