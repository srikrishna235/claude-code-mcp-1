#!/usr/bin/env python3
"""
Test if Claude can actually teach using Scrimba methodology
"""
import subprocess
import json

def test_claude_teaching():
    """Test Claude with a teaching prompt"""
    
    # Build Scrimba-style teaching prompt
    prompt = """You are a Scrimba teacher. Teach variables in JavaScript following this EXACT format:

**20-Second Story:**
[Tell a quick personal story about variables]

**Type THIS Now (60 seconds):**
```javascript
// Create your first variable
let myName = "Student";
console.log(myName);
console.log("I created a variable!");
```

**Your Challenge:**
Create 3 more variables and console.log them all!

Keep it under 200 words. Be enthusiastic!"""
    
    print("Testing Claude with teaching prompt...")
    print("-" * 50)
    
    try:
        # Call Claude with correct syntax
        result = subprocess.run(
            [
                "claude", 
                "-p", prompt,
                "--dangerously-skip-permissions",
                "--output-format", "text"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout:
            print("✅ SUCCESS! Claude responded:")
            print("=" * 50)
            print(result.stdout)
            print("=" * 50)
            return True
        else:
            print("❌ FAILED")
            print("Return code:", result.returncode)
            print("Stderr:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Claude timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_claude_teaching()
    print("\nTest Result:", "✅ PASSED" if success else "❌ FAILED")