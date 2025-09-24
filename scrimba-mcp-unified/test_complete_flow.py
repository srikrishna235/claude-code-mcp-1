#!/usr/bin/env python3
"""
Test Complete Execution Flow
Verifies that frontend → API → Claude flow works with session persistence
"""

import requests
import time
import subprocess
import os
import signal

API_URL = "http://localhost:8002"
FRONTEND_URL = "http://localhost:8003"

def start_servers():
    """Start API and frontend servers"""
    print("Starting servers...")
    
    # Start API server
    api_process = subprocess.Popen(
        ["python", "api-bridge/production_api_session.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start frontend server
    frontend_process = subprocess.Popen(
        ["python", "-m", "http.server", "8003"],
        cwd="api-bridge",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Waiting for servers to start...")
    time.sleep(5)
    
    return api_process, frontend_process

def test_flow():
    """Test the complete flow"""
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE EXECUTION FLOW")
    print("=" * 60)
    
    # Step 1: Check API health
    print("\n1. Checking API health...")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API running")
            print(f"   Active sessions: {data.get('active_sessions', 0)}")
        else:
            print("   ❌ API not healthy")
            return False
    except Exception as e:
        print(f"   ❌ Cannot reach API: {e}")
        return False
    
    # Step 2: Simulate user session (like frontend would)
    print("\n2. Creating user session (simulating frontend)...")
    
    # Generate userId like frontend does
    import uuid
    user_id = str(uuid.uuid4())
    print(f"   Generated userId: {user_id}")
    
    # Step 3: First teaching request
    print("\n3. First teaching request (variables)...")
    response = requests.post(
        f"{API_URL}/api/teach",
        json={"topic": "variables", "step": 1, "user_id": user_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Teaching successful")
        print(f"   Session active: {data.get('session_active')}")
        print(f"   Lesson preview: {data.get('lesson', '')[:100]}...")
    else:
        print(f"   ❌ Teaching failed: {response.status_code}")
        return False
    
    # Step 4: Second request with same userId (should maintain context)
    print("\n4. Second request with same userId (testing context)...")
    response = requests.post(
        f"{API_URL}/api/challenge",
        json={"difficulty": "easy", "user_id": user_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Challenge created")
        print(f"   UserId matches: {data.get('user_id') == user_id}")
        print(f"   Challenge preview: {data.get('challenge', '')[:100]}...")
    else:
        print(f"   ❌ Challenge failed: {response.status_code}")
        return False
    
    # Step 5: Third request (should remember everything)
    print("\n5. Checking code (should remember teaching history)...")
    code = "let myName = 'Test'; console.log(myName);"
    response = requests.post(
        f"{API_URL}/api/check",
        json={"code": code, "user_id": user_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Code checked")
        print(f"   Interactions so far: {data.get('session_interactions', 0)}")
        print(f"   Feedback preview: {data.get('feedback', '')[:100]}...")
    else:
        print(f"   ❌ Check failed: {response.status_code}")
        return False
    
    # Step 6: Get session info
    print("\n6. Verifying session persistence...")
    response = requests.post(f"{API_URL}/api/session/info/{user_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Session persisted!")
        print(f"   Session ID: {data.get('session_id')}")
        print(f"   Total interactions: {data.get('interaction_count')}")
        print(f"   Topics covered: {data.get('topics_covered')}")
    else:
        print(f"   ❌ Session not found")
        return False
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE FLOW WORKING!")
    print("=" * 60)
    
    return True

def test_frontend_integration():
    """Test that frontend properly sends userId"""
    print("\n7. Testing frontend integration...")
    print(f"   Frontend URL: {FRONTEND_URL}/scrimba-learning-app.html")
    print("   ⚠️  Manual test required:")
    print("   1. Open browser console")
    print("   2. Look for 'User session ID:' log")
    print("   3. Click any teaching button")
    print("   4. Check network tab for user_id in requests")

if __name__ == "__main__":
    # Test with existing servers or start new ones
    try:
        # Try to use existing servers first
        print("Testing with existing servers...")
        success = test_flow()
        
        if success:
            test_frontend_integration()
    except requests.exceptions.ConnectionError:
        print("No servers running. Start them with:")
        print("  Terminal 1: cd api-bridge && python production_api_session.py")
        print("  Terminal 2: cd api-bridge && python -m http.server 8003")
        print("")
        print("Or use start_servers() function in this script")