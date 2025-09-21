#!/usr/bin/env python3
"""Test Visual Code Teaching System"""

import asyncio
import sys
sys.path.append('/home/rishabh/Desktop/dev/claude-code-mcp/custom-tool')

from visual_code_mcp import (
    variable_visualizer,
    comparison_visualizer,
    array_visualizer,
    function_sequencer,
    object_visualizer,
    loop_animator,
    set_theme
)

async def test_visual_system():
    print("="*60)
    print("VISUAL CODE TEACHING SYSTEM TEST")
    print("="*60)
    
    # Test 1: Variables
    print("\n📦 TEST 1: Variables (Pokemon Theme)")
    await set_theme("pokemon")
    
    result = await variable_visualizer("pikachu", "0", "assign")
    print(f"pikachu = 0:\n  {result}\n")
    
    result = await variable_visualizer("pikachu", "3", "assign")
    print(f"pikachu = 3:\n  {result}\n")
    
    result = await variable_visualizer("pikachu", "4", "increment")
    print(f"pikachu++:\n  {result}\n")
    
    # Test 2: Comparisons
    print("\n🏁 TEST 2: Comparisons (Racing Theme)")
    await set_theme("racing")
    
    result = await comparison_visualizer("car1", ">", "car2")
    print(f"car1 > car2:\n  {result}\n")
    
    result = await comparison_visualizer("car1", "==", "car2")
    print(f"car1 == car2:\n  {result}\n")
    
    # Test 3: Arrays
    print("\n📚 TEST 3: Arrays")
    await set_theme("pokemon")
    
    result = await array_visualizer("team", "create", None, "6")
    print(f"let team = []:\n  {result}\n")
    
    result = await array_visualizer("team", "assign", 0, "Pikachu")
    print(f"team[0] = 'Pikachu':\n  {result}\n")
    
    result = await array_visualizer("team", "push", None, "Charmander")
    print(f"team.push('Charmander'):\n  {result}\n")
    
    # Test 4: Functions
    print("\n🎬 TEST 4: Functions")
    steps = [
        "Person standing, looking thirsty",
        "Person walking to water cooler",
        "Person picking up glass",
        "Person filling glass with water",
        "Person drinking water",
        "Person with satisfied expression, empty glass"
    ]
    result = await function_sequencer("drinkWater", steps)
    print(f"function drinkWater():\n{result}\n")
    
    # Test 5: Objects
    print("\n🚗 TEST 5: Objects")
    await set_theme("racing")
    
    car_props = {
        "wheels": "4",
        "engine": "V8",
        "color": "red",
        "speed": "200mph"
    }
    result = await object_visualizer("car", car_props)
    print(f"car object:\n{result}\n")
    
    # Test 6: Loops
    print("\n🔄 TEST 6: Loops")
    await set_theme("cooking")
    
    operations = [
        "Adding sugar to bowl",
        "Adding flour to bowl",
        "Mixing ingredients",
        "Baking in oven"
    ]
    result = await loop_animator("for", 4, operations)
    print(f"for loop:\n{result}\n")
    
    print("="*60)
    print("✅ ALL VISUAL TESTS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_visual_system())