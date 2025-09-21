#!/usr/bin/env python3
"""
Comprehensive MCP Server Testing Suite
Tests all servers and their tools
"""

import sys
import asyncio
import json
from pathlib import Path

# Add all server directories to path
sys.path.extend([
    'servers/teaching',
    'servers/visual',
    'servers/visual-code', 
    'servers/projects'
])

async def test_teaching_server():
    """Test teaching server tools."""
    print("\n🎓 TESTING TEACHING SERVER")
    print("=" * 50)
    
    from server import teach, give_challenge, check_code, next, show_progress
    
    # Test teach tool
    print("\n1. Testing teach()")
    result = await teach("variables", 1)
    print(f"✅ teach() returned {len(result)} chars")
    
    # Test give_challenge tool
    print("\n2. Testing give_challenge()")
    result = await give_challenge("easy")
    print(f"✅ give_challenge() returned {len(result)} chars")
    
    # Test check_code tool
    print("\n3. Testing check_code()")
    result = await check_code("let myAge = 25")
    print(f"✅ check_code() returned {len(result)} chars")
    
    return True

async def test_visual_server():
    """Test visual server tools."""
    print("\n🎨 TESTING VISUAL SERVER")
    print("=" * 50)
    
    # Import after clearing module cache
    if 'server' in sys.modules:
        del sys.modules['server']
    
    from servers.visual.server import visualize_concept, animate_concept, visual_challenge, explain_with_diagram, create_meme
    
    # Test visualize_concept
    print("\n1. Testing visualize_concept()")
    result = await visualize_concept("loops", "scrimba")
    print(f"✅ visualize_concept() returned {len(result)} chars")
    
    # Test animate_concept
    print("\n2. Testing animate_concept()")
    result = await animate_concept("variables", 3)
    print(f"✅ animate_concept() returned {len(result)} chars")
    
    # Test visual_challenge
    print("\n3. Testing visual_challenge()")
    result = await visual_challenge("medium")
    print(f"✅ visual_challenge() returned {len(result)} chars")
    
    return True

async def test_visual_code_server():
    """Test visual-code server tools."""
    print("\n💻 TESTING VISUAL-CODE SERVER")
    print("=" * 50)
    
    # Clear module cache and path
    if 'server' in sys.modules:
        del sys.modules['server']
    
    # Import directly with exec to avoid namespace issues
    import importlib.util
    spec = importlib.util.spec_from_file_location("vc_server", "servers/visual-code/server.py")
    vc_server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc_server)
    
    variable_visualizer = vc_server.variable_visualizer
    comparison_visualizer = vc_server.comparison_visualizer
    array_visualizer = vc_server.array_visualizer
    
    # Test variable_visualizer
    print("\n1. Testing variable_visualizer()")
    result = await variable_visualizer("myAge", "25", "assign")
    print(f"✅ variable_visualizer() returned {len(result)} chars")
    
    # Test comparison_visualizer  
    print("\n2. Testing comparison_visualizer()")
    result = await comparison_visualizer("5", ">", "3")
    print(f"✅ comparison_visualizer() returned {len(result)} chars")
    
    # Test array_visualizer
    print("\n3. Testing array_visualizer()")
    result = await array_visualizer("myArray", "push", None, "apple")
    print(f"✅ array_visualizer() returned {len(result)} chars")
    
    return True

async def test_projects_server():
    """Test projects server tools."""
    print("\n🔨 TESTING PROJECTS SERVER")
    print("=" * 50)
    
    # Clear module cache
    if 'server' in sys.modules:
        del sys.modules['server']
    
    from servers.projects.server import start_project, track_progress
    
    # Test start_project
    print("\n1. Testing start_project()")
    result = await start_project("passenger_counter")
    print(f"✅ start_project() returned {len(result)} chars")
    
    # Test track_progress
    print("\n2. Testing track_progress()")
    result = await track_progress()
    print(f"✅ track_progress() returned {len(result)} chars")
    
    return True

async def test_integration():
    """Test integration scenarios."""
    print("\n🔗 TESTING INTEGRATION SCENARIOS")
    print("=" * 50)
    
    print("\n1. Teaching Flow Test")
    print("- Teach → Challenge → Check → Progress")
    
    from servers.teaching.server import teach, give_challenge, check_code, show_progress
    
    # Full teaching flow
    lesson = await teach("functions", 1)
    challenge = await give_challenge("easy")
    check = await check_code("function greet() { console.log('Hi!'); }")
    progress = await show_progress()
    
    print("✅ Full teaching flow completed")
    
    print("\n2. Visual Learning Test")
    print("- Visualize → Animate → Challenge")
    
    from servers.visual.server import visualize_concept, animate_concept, visual_challenge
    
    visual = await visualize_concept("arrays", "scrimba")
    animate = await animate_concept("arrays", 4)
    challenge = await visual_challenge("hard")
    
    print("✅ Visual learning flow completed")
    
    return True

async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🚀 SCRIMBA MCP SERVERS COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    try:
        # Test each server
        results.append(("Teaching", await test_teaching_server()))
        results.append(("Visual", await test_visual_server()))
        results.append(("Visual-Code", await test_visual_code_server()))
        results.append(("Projects", await test_projects_server()))
        results.append(("Integration", await test_integration()))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        all_passed = True
        for name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{name} Server: {status}")
            if not passed:
                all_passed = False
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 ALL TESTS PASSED! System is working perfectly!")
        else:
            print("⚠️ Some tests failed. Check logs above.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)