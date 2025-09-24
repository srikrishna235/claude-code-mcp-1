# 🚀 QUICK FIX REFERENCE CARD

## The Problem in 1 Line
**Unified has no Claude CLI connection = Car without engine**

## The Fix in 3 Commands
```bash
chmod +x fix_unified_phase1.sh
./fix_unified_phase1.sh
# DONE - It works now
```

---

## Manual Fix (If Script Fails)

### 30-Second Fix
```bash
cd /home/rishabh/Desktop/dev/claude-code-mcp
cp claude_code_mcp_final.py scrimba-mcp-unified/
cp terminal.html scrimba-mcp-unified/
cp terminal_server.py scrimba-mcp-unified/
cd scrimba-mcp-unified/
python terminal_server.py
# Open http://localhost:8080
```

---

## What Each Phase Does

| Phase | Time | Adds | Result |
|-------|------|------|---------|
| 1 | 2hr | Claude CLI | Can execute commands |
| 2 | 2hr | Teaching | Scrimba lessons work |
| 3 | 2hr | Visuals | Image prompts work |

---

## Testing Each Phase

### Test Phase 1:
```bash
# In browser at localhost:8080
Type: "What is 2+2?"
Expected: "4"
```

### Test Phase 2:
```bash
Type: "Teach me variables"
Expected: Scrimba-style lesson with console.log
```

### Test Phase 3:
```bash
Type: "Visualize arrays"
Expected: Image generation prompt
```

---

## File Structure (Final)

```
BEFORE: 40+ files, 0% working
AFTER:  5 files, 100% working

scrimba-mcp-unified/
├── claude_code_mcp_final.py  # ENGINE
├── terminal.html              # UI
├── terminal_server.py         # SERVER
├── teaching_server.py         # TEACHING (Phase 2)
└── visual_server.py           # VISUAL (Phase 3)
```

---

## Debug Checklist

Claude not working?
```bash
which claude  # Must show path
npm install -g @anthropic-ai/claude-code
```

Port 8080 in use?
```bash
lsof -i :8080
kill -9 [PID]
```

No response?
```bash
echo $ANTHROPIC_API_KEY  # Must be set
export ANTHROPIC_API_KEY="sk-..."
```

---

## The Core Principle

**"What's the smallest thing I can add that provides value?"**

NOT: "How do I architect this for scale?"

---

## Success Metrics

✅ Phase 1 Success = Can run Claude commands
✅ Phase 2 Success = Can teach with Scrimba style  
✅ Phase 3 Success = Can generate visuals

**If Phase 1 works, SHIP IT!**

---

## Remember

1. Working > Perfect
2. Simple > Complex  
3. Today > Tomorrow
4. 5 files > 50 files

**Make it work. Ship it. Everything else is details.**