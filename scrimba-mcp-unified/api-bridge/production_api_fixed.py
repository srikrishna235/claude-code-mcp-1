#!/usr/bin/env python3
"""
Fixed Production API Server - Actually Works with Claude Code
Following Progressive Enhancement: Make it work FIRST
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Scrimba Teaching API", version="1.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TeachRequest(BaseModel):
    topic: str
    step: int = 1

class ChallengeRequest(BaseModel):
    difficulty: str = "easy"
    topic: Optional[str] = None

class CheckCodeRequest(BaseModel):
    code: str
    challenge: Optional[str] = None

class AdaptiveRequest(BaseModel):
    message: str

# Core function to call Claude
def call_claude(prompt: str) -> str:
    """Call Claude Code CLI with correct syntax"""
    try:
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
            logger.info("Claude responded successfully")
            return result.stdout
        else:
            logger.warning(f"Claude error: {result.stderr}")
            return fallback_response(prompt)
            
    except subprocess.TimeoutExpired:
        logger.error("Claude timed out")
        return fallback_response(prompt)
    except Exception as e:
        logger.error(f"Error calling Claude: {e}")
        return fallback_response(prompt)

def fallback_response(prompt: str) -> str:
    """Simple fallback when Claude isn't available"""
    return f"""🚀 **Scrimba Learning Response**

I'm having trouble connecting to Claude right now, but here's a quick lesson:

**The 60-Second Rule:** Start coding within 60 seconds!

```javascript
// Type this NOW!
console.log("I'm learning by doing!");
```

**Your challenge:** Modify the code above and run it!

*Note: Running in fallback mode - Claude will provide better responses when available*"""

@app.get("/")
async def health_check():
    """Check if API is running and Claude is available"""
    # Test Claude
    test_result = call_claude("Say 'Working'")
    claude_available = "Working" in test_result
    
    return {
        "status": "healthy",
        "claude_available": claude_available,
        "mode": "claude" if claude_available else "fallback"
    }

@app.post("/api/teach")
async def teach(request: TeachRequest):
    """Teach a programming concept using Scrimba methodology"""
    
    prompt = f"""You are a Scrimba teacher. Teach {request.topic} in JavaScript.
    
This is level {request.step}/5 of progressive complexity.

Format your response EXACTLY like this:

**20-Second Story:**
[Brief personal story about the concept]

**Type THIS Now (60 seconds):**
```javascript
// Code they should type immediately
console.log("example");
```

**Your Challenge:**
[Specific task to try right now]

Keep it under 300 words. Be enthusiastic! Use emojis! Remember: Students should be coding within 60 seconds!"""
    
    lesson = call_claude(prompt)
    
    return {
        "lesson": lesson,
        "topic": request.topic,
        "step": request.step,
        "next_step": min(request.step + 1, 5)
    }

@app.post("/api/challenge")
async def get_challenge(request: ChallengeRequest):
    """Get a coding challenge"""
    
    time_limits = {"easy": 60, "medium": 120, "hard": 180}
    time = time_limits.get(request.difficulty, 60)
    
    topic_part = f"about {request.topic}" if request.topic else "for JavaScript beginners"
    
    prompt = f"""Create a {request.difficulty} coding challenge {topic_part}.
    
Time limit: {time} seconds

Format:
⚡ **{time}-SECOND CHALLENGE!**

Task:
[What they need to build]

```javascript
// Starter code
```

Remember: Make it urgent and exciting! They should start typing immediately!"""
    
    challenge = call_claude(prompt)
    
    return {
        "challenge": challenge,
        "difficulty": request.difficulty,
        "time_limit": time
    }

@app.post("/api/check")
async def check_code(request: CheckCodeRequest):
    """Check user's code with encouragement"""
    
    prompt = f"""You are an encouraging Scrimba teacher. Review this code:

```javascript
{request.code}
```

Give feedback following these rules:
1. ALWAYS be positive and encouraging
2. Point out what they did RIGHT first
3. If there are issues, phrase them as "let's try..." suggestions
4. Check if they used console.log (celebrate if they did!)
5. End with excitement for their next step

Keep it brief (under 150 words) and enthusiastic!"""
    
    feedback = call_claude(prompt)
    
    # Check for console.log
    has_console_log = "console.log" in request.code.lower()
    
    return {
        "feedback": feedback,
        "metadata": {
            "has_console_log": has_console_log,
            "line_count": len(request.code.split('\n'))
        }
    }

@app.post("/api/continue")
async def continue_lesson():
    """Continue to next lesson"""
    
    prompt = """Give the next mini-lesson in the Scrimba learning journey.
    
Pick a random next topic from: variables, functions, arrays, loops, objects.
Make it feel like a natural progression.

Use the same format:
- 20-second story
- Code to type NOW
- Challenge

Keep the 60-second urgency!"""
    
    next_lesson = call_claude(prompt)
    
    return {
        "next_lesson": next_lesson
    }

@app.post("/api/adaptive")
async def adaptive_request(request: AdaptiveRequest):
    """Handle any learning request adaptively"""
    
    prompt = f"""You are a Scrimba teacher responding to: "{request.message}"
    
Respond in Scrimba style:
- Personal and enthusiastic
- Include code examples with console.log
- Keep it practical and hands-on
- Maintain the 60-second urgency

If they're asking for help, be encouraging!
If they're asking to learn something, teach it Scrimba-style!"""
    
    response = call_claude(prompt)
    
    return {
        "response": response
    }

@app.post("/api/reset")
async def reset_session():
    """Reset learning session"""
    return {"status": "reset", "message": "Ready for a fresh start! Let's code!"}

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Starting FIXED Production API Server")
    print("✅ Using Claude Code (login auth, not API keys)")
    print("📖 Docs: http://localhost:8002/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8002)