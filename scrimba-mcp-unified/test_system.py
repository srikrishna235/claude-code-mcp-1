#!/usr/bin/env python3
"""
Test script for Scrimba Teaching MCP System
"""

import sys
import asyncio
sys.path.insert(0, 'teaching-server')

from teaching_mcp import teach, give_challenge, check_code, next_lesson, start_project, visualize_concept, show_progress

async def test_teaching_system():
    """Test all teaching functions."""
    print("="*60)
    print("TESTING SCRIMBA TEACHING MCP SYSTEM")
    print("="*60)
    
    # Test 1: Teach
    print("\n1. TESTING TEACH FUNCTION:")
    print("-"*40)
    result = await teach("variables", 1)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test 2: Give Challenge
    print("\n2. TESTING GIVE CHALLENGE:")
    print("-"*40)
    result = await give_challenge("easy")
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Test 3: Check Code
    print("\n3. TESTING CHECK CODE:")
    print("-"*40)
    result = await check_code("let myAge = 25")
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Test 4: Next Lesson
    print("\n4. TESTING NEXT LESSON:")
    print("-"*40)
    result = await next_lesson()
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Test 5: Start Project
    print("\n5. TESTING START PROJECT:")
    print("-"*40)
    result = await start_project("passenger_counter")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test 6: Visualize Concept
    print("\n6. TESTING VISUALIZE CONCEPT:")
    print("-"*40)
    result = await visualize_concept("variables")
    print(result[:400] + "..." if len(result) > 400 else result)
    
    # Test 7: Show Progress
    print("\n7. TESTING SHOW PROGRESS:")
    print("-"*40)
    result = await show_progress()
    print(result[:400] + "..." if len(result) > 400 else result)
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_teaching_system())