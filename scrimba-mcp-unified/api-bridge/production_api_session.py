#!/usr/bin/env python3
"""
Session-Aware Production API Server
Maintains context using Claude Code's --resume feature
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import subprocess
import json
import logging
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Scrimba Teaching API with Sessions", version="2.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage (in production, use Redis or database)
SESSIONS: Dict[str, Dict] = {}

# Request models
class TeachRequest(BaseModel):
    topic: str
    step: int = 1
    user_id: Optional[str] = None

class ChallengeRequest(BaseModel):
    difficulty: str = "easy"
    topic: Optional[str] = None
    user_id: Optional[str] = None

class CheckCodeRequest(BaseModel):
    code: str
    challenge: Optional[str] = None
    user_id: Optional[str] = None

class AdaptiveRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

def get_or_create_session(user_id: Optional[str] = None) -> tuple[str, str]:
    """Get existing session or create new one"""
    
    # Use provided user_id or generate one
    if not user_id:
        user_id = str(uuid.uuid4())
    
    # Check if user has existing session
    if user_id in SESSIONS:
        session_data = SESSIONS[user_id]
        logger.info(f"Resuming session {session_data['claude_session_id']} for user {user_id}")
        return user_id, session_data['claude_session_id']
    
    # No existing session, will create new one on first Claude call
    logger.info(f"New user {user_id}, will create session on first call")
    return user_id, None

def call_claude_with_session(prompt: str, user_id: str, session_id: Optional[str] = None) -> tuple[str, str]:
    """
    Call Claude and maintain session context
    Returns: (response_text, session_id)
    """
    try:
        # Build command
        cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions", "--output-format", "json"]
        
        # If we have a session_id, resume it
        if session_id:
            cmd.extend(["--resume", session_id])
            logger.info(f"Resuming Claude session: {session_id}")
        else:
            logger.info("Starting new Claude session")
        
        # Execute Claude
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout:
            # Parse JSON response
            response_data = json.loads(result.stdout)
            
            # Extract session_id and response
            new_session_id = response_data.get("session_id")
            response_text = response_data.get("result", "")
            
            # Store session info
            if new_session_id and user_id not in SESSIONS:
                SESSIONS[user_id] = {
                    "claude_session_id": new_session_id,
                    "created_at": datetime.now().isoformat(),
                    "last_interaction": datetime.now().isoformat(),
                    "interaction_count": 1,
                    "topics_covered": []
                }
                logger.info(f"Created new session {new_session_id} for user {user_id}")
            elif new_session_id:
                # Update existing session
                SESSIONS[user_id]["last_interaction"] = datetime.now().isoformat()
                SESSIONS[user_id]["interaction_count"] += 1
            
            return response_text, new_session_id
            
        else:
            logger.error(f"Claude error: {result.stderr}")
            return fallback_response(prompt), None
            
    except subprocess.TimeoutExpired:
        logger.error("Claude timed out")
        return fallback_response(prompt), None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude JSON: {e}")
        # Try to extract text response
        if result.stdout:
            return result.stdout, session_id
        return fallback_response(prompt), None
    except Exception as e:
        logger.error(f"Error calling Claude: {e}")
        return fallback_response(prompt), None

def fallback_response(prompt: str) -> str:
    """Fallback when Claude isn't available"""
    return f"""🚀 **Scrimba Learning Response**

I'm having trouble connecting to Claude, but here's a quick lesson:

**60-Second Challenge:** Start coding NOW!

```javascript
console.log("Keep learning!");
```

*Note: Session context unavailable in fallback mode*"""

@app.get("/")
async def health_check():
    """Check API health and session status"""
    return {
        "status": "healthy",
        "active_sessions": len(SESSIONS),
        "sessions": {
            user_id: {
                "created": data["created_at"],
                "interactions": data["interaction_count"],
                "last_active": data["last_interaction"]
            }
            for user_id, data in SESSIONS.items()
        }
    }

@app.post("/api/teach")
async def teach(request: TeachRequest):
    """Teach with session context"""
    
    # Get or create session
    user_id, session_id = get_or_create_session(request.user_id)
    
    # Build context-aware prompt
    prompt = f"""You are a Scrimba teacher in an ongoing learning session.
    
Current topic: {request.topic}
Complexity level: {request.step}/5

If you've taught this student before, reference previous lessons briefly.
If this is a new student, introduce yourself warmly.

Format your response:

**20-Second Story:**
[Personal story related to the topic]

**Type THIS Now (60 seconds):**
```javascript
// Code to type immediately
console.log("example");
```

**Your Challenge:**
[Immediate task to complete]

Be enthusiastic and maintain continuity with previous lessons if any."""
    
    # Call Claude with session
    lesson, new_session_id = call_claude_with_session(prompt, user_id, session_id)
    
    # Track topic in session
    if user_id in SESSIONS:
        if request.topic not in SESSIONS[user_id]["topics_covered"]:
            SESSIONS[user_id]["topics_covered"].append(request.topic)
    
    return {
        "lesson": lesson,
        "topic": request.topic,
        "step": request.step,
        "user_id": user_id,
        "session_active": user_id in SESSIONS,
        "topics_covered": SESSIONS.get(user_id, {}).get("topics_covered", [])
    }

@app.post("/api/challenge")
async def get_challenge(request: ChallengeRequest):
    """Get challenge with context"""
    
    user_id, session_id = get_or_create_session(request.user_id)
    
    time_limits = {"easy": 60, "medium": 120, "hard": 180}
    time = time_limits.get(request.difficulty, 60)
    
    # Context-aware prompt
    context = ""
    if user_id in SESSIONS and SESSIONS[user_id].get("topics_covered"):
        topics = SESSIONS[user_id]["topics_covered"]
        context = f"This student has learned: {', '.join(topics)}. Build on that knowledge."
    
    prompt = f"""Create a {request.difficulty} coding challenge.

{context}

Time limit: {time} seconds

Format:
⚡ **{time}-SECOND CHALLENGE!**

Make it relevant to what the student has learned so far."""
    
    challenge, _ = call_claude_with_session(prompt, user_id, session_id)
    
    return {
        "challenge": challenge,
        "difficulty": request.difficulty,
        "time_limit": time,
        "user_id": user_id
    }

@app.post("/api/check")
async def check_code(request: CheckCodeRequest):
    """Check code with session context"""
    
    user_id, session_id = get_or_create_session(request.user_id)
    
    prompt = f"""Review this student's code. You've been teaching them, so reference their progress.

Code:
```javascript
{request.code}
```

Give encouraging feedback that shows you remember their learning journey.
Celebrate their progress from where they started!"""
    
    feedback, _ = call_claude_with_session(prompt, user_id, session_id)
    
    return {
        "feedback": feedback,
        "user_id": user_id,
        "session_interactions": SESSIONS.get(user_id, {}).get("interaction_count", 0)
    }

@app.post("/api/continue")
async def continue_lesson(user_id: Optional[str] = None):
    """Continue learning journey"""
    
    user_id, session_id = get_or_create_session(user_id)
    
    if not session_id:
        return {
            "next_lesson": "Welcome! Let's start your learning journey. What would you like to learn first?",
            "user_id": user_id
        }
    
    prompt = """Continue teaching this student. 
    Reference what they've learned so far and suggest the next logical step.
    Keep the Scrimba format with code to type in 60 seconds!"""
    
    next_lesson, _ = call_claude_with_session(prompt, user_id, session_id)
    
    return {
        "next_lesson": next_lesson,
        "user_id": user_id,
        "topics_covered": SESSIONS.get(user_id, {}).get("topics_covered", [])
    }

@app.post("/api/adaptive")
async def adaptive_request(request: AdaptiveRequest):
    """Handle any request with full context"""
    
    user_id, session_id = get_or_create_session(request.user_id)
    
    prompt = f"""Student message: "{request.message}"

Respond as their Scrimba teacher who knows their full learning history.
Be personal, reference past lessons if relevant, and keep the 60-second coding momentum!"""
    
    response, _ = call_claude_with_session(prompt, user_id, session_id)
    
    return {
        "response": response,
        "user_id": user_id
    }

@app.post("/api/session/info/{user_id}")
async def get_session_info(user_id: str):
    """Get session information"""
    
    if user_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = SESSIONS[user_id]
    return {
        "user_id": user_id,
        "session_id": session_data["claude_session_id"],
        "created_at": session_data["created_at"],
        "last_interaction": session_data["last_interaction"],
        "interaction_count": session_data["interaction_count"],
        "topics_covered": session_data["topics_covered"]
    }

@app.delete("/api/session/{user_id}")
async def end_session(user_id: str):
    """End a learning session"""
    
    if user_id in SESSIONS:
        session_data = SESSIONS.pop(user_id)
        return {
            "message": "Session ended",
            "total_interactions": session_data["interaction_count"],
            "topics_covered": session_data["topics_covered"]
        }
    
    return {"message": "No session found"}

@app.post("/api/reset")
async def reset_all_sessions():
    """Reset all sessions (for testing)"""
    count = len(SESSIONS)
    SESSIONS.clear()
    return {"message": f"Cleared {count} sessions"}

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Session-Aware Production API Server")
    print("✅ Maintains context using Claude --resume")
    print("📖 Docs: http://localhost:8002/docs")
    print("=" * 60)
    print("Session Management:")
    print("- Each user gets a unique session")
    print("- Context maintained across all interactions")
    print("- Claude remembers everything in the session")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8002)