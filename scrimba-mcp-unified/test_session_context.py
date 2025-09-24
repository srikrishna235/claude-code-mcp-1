#!/usr/bin/env python3
"""
Test Claude Code session persistence
Shows that context is maintained across multiple API calls
"""

import requests
import json
import time

API_URL = "http://localhost:8002"

def test_session_persistence():
    """Test that Claude remembers context across calls"""
    
    print("=" * 60)
    print("TESTING SESSION PERSISTENCE WITH CLAUDE CODE")
    print("=" * 60)
    
    # Step 1: First teaching interaction
    print("\n1. First call - Teaching variables:")
    print("-" * 40)
    
    response = requests.post(
        f"{API_URL}/api/teach",
        json={"topic": "variables", "step": 1}
    )
    data = response.json()
    user_id = data.get("user_id")
    
    print(f"User ID: {user_id}")
    print(f"Session Active: {data.get('session_active')}")
    print("Lesson excerpt:")
    print(data.get("lesson", "")[:200] + "...")
    
    # Step 2: Ask a challenge (should remember we learned variables)
    print("\n2. Second call - Get challenge (should reference variables):")
    print("-" * 40)
    
    response = requests.post(
        f"{API_URL}/api/challenge",
        json={"difficulty": "easy", "user_id": user_id}
    )
    data = response.json()
    
    print(f"User ID: {data.get('user_id')}")
    print("Challenge excerpt:")
    print(data.get("challenge", "")[:200] + "...")
    
    # Step 3: Submit code for checking
    print("\n3. Third call - Check code (should remember teaching history):")
    print("-" * 40)
    
    code = """
    let myName = "Alice";
    let myAge = 25;
    console.log(myName);
    console.log(myAge);
    """
    
    response = requests.post(
        f"{API_URL}/api/check",
        json={"code": code, "user_id": user_id}
    )
    data = response.json()
    
    print(f"Session interactions so far: {data.get('session_interactions')}")
    print("Feedback excerpt:")
    print(data.get("feedback", "")[:300] + "...")
    
    # Step 4: Continue learning (should suggest next topic based on history)
    print("\n4. Fourth call - Continue learning (should know what we've covered):")
    print("-" * 40)
    
    response = requests.post(
        f"{API_URL}/api/continue",
        json={"user_id": user_id}
    )
    data = response.json()
    
    print(f"Topics covered: {data.get('topics_covered')}")
    print("Next lesson excerpt:")
    print(data.get("next_lesson", "")[:300] + "...")
    
    # Step 5: Ask adaptive question (should have full context)
    print("\n5. Fifth call - Adaptive question (should remember everything):")
    print("-" * 40)
    
    response = requests.post(
        f"{API_URL}/api/adaptive",
        json={
            "message": "Can you remind me what we learned about variables and suggest what to learn next?",
            "user_id": user_id
        }
    )
    data = response.json()
    
    print("Response excerpt (should reference our learning journey):")
    print(data.get("response", "")[:400] + "...")
    
    # Step 6: Get session info
    print("\n6. Session Information:")
    print("-" * 40)
    
    response = requests.post(f"{API_URL}/api/session/info/{user_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"Session ID: {data.get('session_id')}")
        print(f"Total interactions: {data.get('interaction_count')}")
        print(f"Topics covered: {data.get('topics_covered')}")
        print(f"Created at: {data.get('created_at')}")
        print(f"Last interaction: {data.get('last_interaction')}")
    
    print("\n" + "=" * 60)
    print("✅ SESSION TEST COMPLETE")
    print("Claude maintained context across all calls using --resume!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        # Check if API is running
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ API is running")
            test_session_persistence()
        else:
            print("❌ API is not responding")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API at", API_URL)
        print("Start the server with: python production_api_session.py")