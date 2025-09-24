# Claude Code Session Management Guide

## How Session Persistence Works

Claude Code maintains conversation context using session IDs, allowing it to remember everything from previous interactions.

---

## Key Commands

### 1. Start New Session (Auto-generated)
```bash
claude -p "prompt" --output-format json
# Returns: {..., "session_id": "uuid-here", ...}
```

### 2. Resume Specific Session
```bash
claude --resume <session-id> -p "next prompt" --output-format json
# Claude remembers everything from that session
```

### 3. Continue Most Recent Session
```bash
claude -c -p "continue our conversation"
# Continues the last conversation
```

---

## Implementation in Production API

### Architecture
```
User Request
    ↓
API Server (stores session mapping)
    ↓
Claude CLI with --resume <session-id>
    ↓
Claude (maintains full context)
```

### Session Flow

1. **First Interaction:**
   - User sends request without user_id
   - API generates user_id
   - Calls Claude without --resume
   - Captures session_id from response
   - Stores mapping: user_id → session_id

2. **Subsequent Interactions:**
   - User sends request with user_id
   - API retrieves stored session_id
   - Calls Claude with --resume <session-id>
   - Claude remembers entire conversation

---

## Code Example

### Basic Session Management
```python
# First call - start session
result = subprocess.run([
    "claude", "-p", "Teach me variables",
    "--output-format", "json"
], capture_output=True, text=True)

data = json.loads(result.stdout)
session_id = data["session_id"]  # Save this!

# Second call - resume session
result = subprocess.run([
    "claude", "--resume", session_id,
    "-p", "What did we just learn?",
    "--output-format", "json"
], capture_output=True, text=True)

# Claude remembers teaching variables!
```

### API Implementation (Simplified)
```python
SESSIONS = {}  # user_id -> session_id mapping

def call_claude_with_session(prompt, user_id):
    cmd = ["claude", "-p", prompt, "--output-format", "json"]
    
    # Resume existing session if available
    if user_id in SESSIONS:
        cmd.extend(["--resume", SESSIONS[user_id]])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    # Store session for future use
    if user_id not in SESSIONS:
        SESSIONS[user_id] = data["session_id"]
    
    return data["result"]
```

---

## Test Results

### Session Persistence Test
```
Call 1: Teach variables
  → Claude teaches variables
  → Session ID: a22791f8-52a4-4d0e-91ff-12013f285188

Call 2: Get challenge  
  → Claude creates challenge about variables (remembers!)

Call 3: Check code
  → Claude references "when we started" (context!)

Call 4: Continue learning
  → Claude suggests next topic based on history

Call 5: Ask about progress
  → Claude recalls entire learning journey
```

---

## Benefits of Session Management

1. **Continuous Learning Journey**
   - Student progress tracked
   - Personalized teaching based on history
   - Natural conversation flow

2. **Context-Aware Responses**
   - References previous examples
   - Builds on learned concepts
   - Remembers student's name/preferences

3. **Progressive Complexity**
   - Knows what's been covered
   - Suggests logical next steps
   - Avoids repetition

---

## Usage with Frontend

### Modified Frontend (Add user tracking)
```javascript
// Generate or retrieve user ID
let userId = localStorage.getItem('userId');
if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem('userId', userId);
}

// Include in all API calls
fetch('/api/teach', {
    method: 'POST',
    body: JSON.stringify({
        topic: 'arrays',
        step: 1,
        user_id: userId  // Important!
    })
});
```

---

## Files Created

1. **production_api_session.py** - Session-aware API server
2. **test_session_context.py** - Demonstrates persistence
3. **This guide** - Documentation

---

## How to Run

### Start Session-Aware API:
```bash
cd scrimba-mcp-unified/api-bridge
python production_api_session.py
# Runs on http://localhost:8002
```

### Test Session Persistence:
```bash
python test_session_context.py
# Shows 5 sequential calls with maintained context
```

### View Active Sessions:
```bash
curl http://localhost:8002/
# Shows all active sessions and stats
```

---

## Important Notes

1. **Session Storage:** Currently in-memory (lost on restart)
   - Production: Use Redis or database

2. **Session Timeout:** Claude sessions persist for hours
   - Consider implementing cleanup for old sessions

3. **Cost Consideration:** Each --resume still uses tokens
   - But provides much better user experience

4. **Multiple Users:** Each user gets unique session
   - Scalable to thousands of concurrent learners

---

## Summary

**Key Insight:** Use `--resume <session-id>` to maintain full conversation context

**Result:** Claude remembers everything - creates a true learning journey where each interaction builds on the previous ones!