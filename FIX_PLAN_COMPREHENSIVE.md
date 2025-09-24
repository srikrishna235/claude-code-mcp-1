# Comprehensive Fix Plan: Scrimba-MCP-Unified
## Following Progressive Enhancement Methodology Strictly

---

## Pre-Flight Assessment

### Current State Analysis
```
WORKING (Main Project):
✓ claude_code_mcp_final.py - Claude CLI wrapper
✓ terminal.html - Browser interface
✓ Direct test capability
✓ Simple structure

BROKEN (Unified):
✗ No Claude CLI connection
✗ Duplicate servers (v1, v2)
✗ Invalid paths in .mcp.json
✗ Cannot execute ANY Claude commands
```

### Core Principle Violations to Fix
1. **"Ship Every Phase"** - Currently nothing ships
2. **"Make it work first"** - Built features before core
3. **"No premature abstraction"** - Over-nested directories
4. **"Fast feedback"** - No way to test

---

## Logic Flow (How It Should Work)

```
User Request
    ↓
[Browser/Terminal Interface]
    ↓
[MCP Server Entry Point]
    ↓
[Claude CLI Wrapper] ← MISSING!
    ↓
[Claude Executes with Tools]
    ↓
[Response Back to User]
```

### Current Broken Flow
```
User Request
    ↓
[API Bridge] 
    ↓
[Production API]
    ↓
[Tries to call 'claude' command]
    ↓
✗ FAILS - No connection to actual Claude
```

---

## Phase-by-Phase Fix Plan

### PHASE 1: Make Core Work (Day 1 - 2 hours)
**Goal:** Basic Claude CLI execution working

#### Checklist:
- [ ] Copy core files from main to unified
- [ ] Test Claude CLI wrapper standalone
- [ ] Verify terminal interface loads
- [ ] Execute one simple command successfully

#### Execution Steps:
```bash
# Step 1.1: Copy core engine files
cd /home/rishabh/Desktop/dev/claude-code-mcp
cp claude_code_mcp_final.py scrimba-mcp-unified/
cp terminal_server.py scrimba-mcp-unified/
cp terminal.html scrimba-mcp-unified/

# Step 1.2: Test Claude CLI availability
cd scrimba-mcp-unified/
which claude  # Must return path
claude --version  # Must show version

# Step 1.3: Start MCP server
python claude_code_mcp_final.py

# Step 1.4: In another terminal, start web server
python terminal_server.py

# Step 1.5: Open browser
# Navigate to http://localhost:8080
# Test: "What is 2+2?"
```

#### Success Criteria:
- Can execute: `claude_execute("what is 2+2")`
- Get response: "4"
- Terminal shows execution

#### Rollback Point:
- If fails, check Claude CLI installation
- Verify with: `npm list -g @anthropic-ai/claude-code`

---

### PHASE 2: Single Teaching Server (Day 1 - 2 hours)
**Goal:** One working teaching server with Claude integration

#### Checklist:
- [ ] Remove ALL duplicate servers
- [ ] Keep only ONE teaching server
- [ ] Connect to Claude CLI wrapper
- [ ] Test teaching a concept

#### Execution Steps:
```bash
# Step 2.1: Clean up duplicates
cd scrimba-mcp-unified/

# Remove v1 servers (keep v2)
rm -rf teaching-server/
rm -rf cli-wrapper/

# Step 2.2: Create single teaching server
cat > teaching_server.py << 'EOF'
#!/usr/bin/env python3
"""Single Teaching Server - Phase 2"""
from mcp.server.fastmcp import FastMCP
import subprocess
import json

mcp = FastMCP("scrimba-teacher")

@mcp.tool()
async def teach_concept(topic: str, step: int = 1) -> str:
    """Teach programming concept using Scrimba methodology"""
    
    # Build Scrimba-style prompt
    prompt = f"""
    Teach {topic} using Scrimba methodology:
    1. 20-second personal hook
    2. Code to type in 60 seconds
    3. Console.log everything
    4. Immediate challenge
    Level: {step}/5
    """
    
    # Call Claude via wrapper
    cmd = ["python", "claude_code_mcp_final.py"]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request
    request = {
        "method": "claude_execute",
        "params": {"prompt": prompt}
    }
    
    stdout, stderr = process.communicate(
        input=json.dumps(request)
    )
    
    return stdout

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run())
EOF

# Step 2.3: Update .mcp.json
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "claude-core": {
      "command": "python",
      "args": ["claude_code_mcp_final.py"]
    },
    "scrimba-teacher": {
      "command": "python", 
      "args": ["teaching_server.py"]
    }
  }
}
EOF

# Step 2.4: Test teaching
python teaching_server.py
# In another terminal:
# Test teach_concept("variables", 1)
```

#### Success Criteria:
- Teaching server starts
- Can teach "variables" 
- Returns Scrimba-style lesson
- Console.log examples included

---

### PHASE 3: Add Visual Server (Day 2 - 2 hours)
**Goal:** Add visual learning capabilities

#### Checklist:
- [ ] Add single visual server
- [ ] Connect to Claude for prompts
- [ ] Generate image descriptions
- [ ] Test visual explanation

#### Execution Steps:
```bash
# Step 3.1: Create visual server
cat > visual_server.py << 'EOF'
#!/usr/bin/env python3
"""Visual Learning Server - Phase 3"""
from mcp.server.fastmcp import FastMCP
import subprocess
import json

mcp = FastMCP("scrimba-visual")

@mcp.tool()
async def visualize_concept(concept: str) -> str:
    """Generate visual explanation prompt"""
    
    prompt = f"""
    Create detailed image generation prompt for teaching {concept}.
    Make it colorful, clear, and engaging.
    Use metaphors and real-world examples.
    """
    
    # Reuse Claude wrapper
    cmd = ["python", "claude_code_mcp_final.py"]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    request = {
        "method": "claude_execute",
        "params": {"prompt": prompt}
    }
    
    stdout, _ = process.communicate(
        input=json.dumps(request)
    )
    
    return stdout

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run())
EOF

# Step 3.2: Update .mcp.json
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "claude-core": {
      "command": "python",
      "args": ["claude_code_mcp_final.py"]
    },
    "scrimba-teacher": {
      "command": "python",
      "args": ["teaching_server.py"]
    },
    "scrimba-visual": {
      "command": "python",
      "args": ["visual_server.py"]
    }
  }
}
EOF

# Step 3.3: Test visual
python visual_server.py
# Test visualize_concept("arrays")
```

#### Success Criteria:
- Visual server starts
- Generates image prompts
- Connects to Claude successfully

---

## Execution Flow Diagram

```
PHASE 1 (Core):
Start → Copy Files → Test Claude CLI → Start Server → Verify in Browser
         ↓ FAIL: Check Claude installation

PHASE 2 (Teaching):  
Phase 1 Works → Remove Duplicates → Create Single Server → Test Teaching
                ↓ FAIL: Rollback to Phase 1

PHASE 3 (Visual):
Phase 2 Works → Add Visual Server → Test Visualization → Ship
                ↓ FAIL: Keep Phase 2 working
```

---

## Testing Strategy Per Phase

### Phase 1 Tests:
```bash
# Test 1: CLI works
echo '{"method":"claude_execute","params":{"prompt":"say hello"}}' | python claude_code_mcp_final.py

# Test 2: Browser works
curl http://localhost:8080/terminal.html

# Test 3: Execute command
# In browser: Type "hello" and press Enter
```

### Phase 2 Tests:
```bash
# Test 1: Server starts
python teaching_server.py &
sleep 2
ps aux | grep teaching_server

# Test 2: Teach concept
# Use MCP client to call teach_concept("variables", 1)

# Test 3: Verify Scrimba format
# Response must have:
# - Personal story
# - console.log examples
# - 60-second timer mention
```

### Phase 3 Tests:
```bash
# Test 1: Visual server starts
python visual_server.py &

# Test 2: Generate prompt
# Call visualize_concept("loops")

# Test 3: Verify description
# Must describe visual elements
# Must be suitable for image generation
```

---

## File Organization (Final Structure)

```
scrimba-mcp-unified/
├── claude_code_mcp_final.py    # Core (Phase 1)
├── teaching_server.py           # Teaching (Phase 2)
├── visual_server.py             # Visual (Phase 3)
├── terminal.html                # Testing interface
├── terminal_server.py           # Web server
├── .mcp.json                    # Clean config
├── api-bridge/                  # Keep for frontend
│   └── scrimba-learning-app.html
└── DEPRECATED/                  # Move old stuff here
    ├── servers/                 # Old v1/v2 servers
    └── teaching-server/         # Old structure
```

---

## Common Issues & Solutions

### Issue 1: Claude CLI not found
```bash
# Fix:
npm install -g @anthropic-ai/claude-code
export PATH=$PATH:~/.npm-global/bin
```

### Issue 2: Port already in use
```bash
# Fix:
lsof -i :8080
kill -9 [PID]
```

### Issue 3: MCP server won't start
```bash
# Fix:
pip install mcp fastmcp
python -m pip install --upgrade mcp
```

### Issue 4: No response from Claude
```bash
# Fix:
# Check API key
echo $ANTHROPIC_API_KEY
# Set if missing
export ANTHROPIC_API_KEY="your-key"
```

---

## Rollback Points

1. **Phase 1 Fails** → Use main project version
2. **Phase 2 Fails** → Keep Phase 1, skip teaching
3. **Phase 3 Fails** → Ship with Phase 1+2 only

---

## Success Metrics

### Phase 1: ✓ Can execute Claude commands
### Phase 2: ✓ Can teach programming concepts  
### Phase 3: ✓ Can generate visual explanations

**Total Time:** 6 hours max
**Files Changed:** 5 new, rest deleted/moved
**Final LOC:** <1000 total (per methodology)

---

## Next Actions (Ordered)

1. **NOW:** Copy claude_code_mcp_final.py
2. **Test:** Verify Claude CLI works
3. **Clean:** Remove duplicate servers
4. **Build:** Single teaching server
5. **Test:** Teaching works
6. **Add:** Visual if time permits
7. **Ship:** Working version today

---

## The Key Insight

**We're not fixing, we're SIMPLIFYING.**

From: 40+ files across multiple directories
To: 5 files that actually work

Remember: "Simple foundation + Progressive enhancement + Fast feedback = Success"