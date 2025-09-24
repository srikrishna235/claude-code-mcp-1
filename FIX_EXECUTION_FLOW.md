# Fix Execution Flow - Systematic Approach

## 🔴 CURRENT BROKEN FLOW

```
User clicks "Teach Variables"
    ↓
Frontend (scrimba-learning-app.html)
    ↓
fetch('/api/teach', {topic: 'variables'})  [NO user_id!]
    ↓
API (production_api_session.py)
    ↓
Creates NEW user_id every time (no persistence!)
    ↓
Claude responds (but starts fresh each time)
    ↓
User refreshes page
    ↓
❌ Everything forgotten - new session starts
```

## ✅ CORRECT LOGIC FLOW

```
User clicks "Teach Variables"
    ↓
Frontend checks localStorage for userId
    ↓ (exists?)     ↓ (doesn't exist?)
    Use it         Generate new UUID
    ↓               ↓
    └─────┬─────────┘
          ↓
fetch('/api/teach', {topic: 'variables', user_id: 'abc-123'})
    ↓
API receives user_id
    ↓
Checks if session exists for user_id
    ↓ (yes)              ↓ (no)
    Resume session       Start new session
    ↓                    ↓
claude --resume <id>     claude -p "prompt"
    ↓
Claude remembers everything!
```

## 🔧 FIX SEQUENCE (Order Matters!)

### DEPENDENCY CHAIN:
```
1. Frontend userId → enables → Session persistence
                     ↓
2. Session persistence → enables → Context maintenance
                         ↓
3. Context → enables → Progressive learning
             ↓
4. MCP servers → need → Claude connection
                 ↓
5. Claude connection → enables → Intelligent responses
```

---

## 📝 FIX #1: Frontend User Session

### Current Problem:
```javascript
// Every API call creates new user
fetch('/api/teach', {
    body: JSON.stringify({
        topic: 'variables',
        step: 1
        // NO user_id - API generates new one!
    })
})
```

### The Fix: