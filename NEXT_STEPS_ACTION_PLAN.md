# Next Steps Action Plan
## What to Fix Next (In Priority Order)

---

## 🔥 IMMEDIATE (Do Right Now - 10 minutes)

### 1. Fix Frontend Session Management
```javascript
// Add to scrimba-learning-app.html line ~394
const sessionStartRef = React.useRef(Date.now());
const userIdRef = React.useRef(
    localStorage.getItem('userId') || crypto.randomUUID()
);
React.useEffect(() => {
    localStorage.setItem('userId', userIdRef.current);
}, []);

// Modify all fetch calls to include:
body: JSON.stringify({
    ...otherData,
    user_id: userIdRef.current
})
```

### 2. Clean Up Structure
```bash
rm -rf DEPRECATED_BACKUP/
rm .mcp.json.backup
```

---

## ⚡ QUICK WINS (Next 30 minutes)

### 3. Fix ONE MCP Server as Proof of Concept
```python
# Edit servers/teaching/server.py
# Add at top:
import subprocess
import json

# Modify teach function to call Claude:
def teach_with_claude(topic, step):
    prompt = f"Teach {topic} using Scrimba methodology..."
    result = subprocess.run([
        "claude", "-p", prompt,
        "--dangerously-skip-permissions"
    ], capture_output=True, text=True)
    return result.stdout
```

### 4. Update .mcp.json
```json
{
  "mcpServers": {
    "claude-core": {
      "command": "python",
      "args": ["claude_code_mcp_final.py"]
    },
    "scrimba-teaching": {
      "command": "python",
      "args": ["servers/teaching/server_fixed.py"]
    }
  }
}
```

---

## 📈 PHASE 2 (If Time Permits - 2 hours)

### 5. Fix All MCP Servers
- Copy the pattern from teaching server
- Apply to visual, visual-code, projects servers
- Test each independently

### 6. Wire Agent Orchestration
- Ensure Task tool can call MCP servers
- Test orchestrator routing
- Verify agent boundaries work

---

## ✅ VALIDATION CHECKLIST

After each fix, verify:
- [ ] Frontend maintains userId across refreshes
- [ ] API maintains session context
- [ ] MCP server responds when called
- [ ] Claude provides actual responses (not fallback)

---

## 🎯 SUCCESS METRICS

You'll know it's working when:
1. Refresh page → Still remembers user
2. Teach topic → Get real Claude response
3. Ask followup → Claude remembers context
4. MCP servers → Actually use Claude intelligence

---

## ⚠️ DON'T DO (Avoid These)

1. **Don't add more features** - Fix existing first
2. **Don't create new servers** - Fix current ones
3. **Don't refactor** - Make it work first
4. **Don't add TypeScript** - Keep it simple
5. **Don't add databases** - localStorage is fine

---

## 🚀 THE ONE THING

If you only have 5 minutes:
**Add userId to frontend** - This alone makes the experience 10x better by maintaining context.

```javascript
// Literally just add this to scrimba-learning-app.html:
const userId = localStorage.getItem('userId') || crypto.randomUUID();
localStorage.setItem('userId', userId);
// Then include user_id: userId in all fetches
```

---

## 📝 Command to Test Everything

```bash
# After making changes:
cd scrimba-mcp-unified/api-bridge
python production_api_session.py &

python -m http.server 8003 &

# Open: http://localhost:8003/scrimba-learning-app.html
# Click "Variables" → Should maintain context across calls
```

---

## Remember the Methodology

**Make it work → Ship it → Use it → Find pain → Fix only that**

Current pain: No session persistence in frontend
Fix: Add userId (5 minutes)
Ship: Test immediately
Next pain: Find and fix