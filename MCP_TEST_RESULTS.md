# MCP Server Test Results

## Test Summary

### ✅ What Works

1. **Simple MCP Server (No Claude calls)**
   - `simple_test_server.py` works perfectly
   - Claude can see tools: `mcp__simple-test__test_echo`, `mcp__simple-test__test_math`
   - Claude can call them successfully:
     - `test_echo('Hello MCP')` → Returns "Echo: Hello MCP"
     - `test_math(5, 3)` → Returns "Result: 5 + 3 = 8"

2. **MCP Server Registration**
   - `claude mcp add` works correctly
   - Claude recognizes MCP tools (shows them in tool list)
   - STDIO communication protocol works

3. **Direct Function Calls**
   - When called directly in Python, `teach_concept()` works
   - Claude CLI responds correctly when called directly
   - Function returns proper Scrimba-style content

### ❌ What Doesn't Work

1. **MCP Server with Claude Subprocess Calls**
   - `server_claude.py` times out when called via MCP
   - All tools that call Claude subprocess hang:
     - `mcp__scrimba-teaching__teach_concept` - timeout
     - `mcp__scrimba-teaching__celebrate` - timeout
     - All other tools that use `call_claude()` - timeout

## Root Cause Analysis

### The Problem: Recursive Claude Calls

```
Claude (main process)
  ↓ calls
MCP Tool (subprocess)
  ↓ tries to call
Claude CLI (another subprocess)
  ↓ waits indefinitely
```

**Why it fails:**
1. Claude calls MCP tool via subprocess
2. MCP tool tries to call Claude CLI
3. This creates a recursive/nested Claude call
4. The inner Claude call may be waiting for resources locked by outer Claude
5. Result: Deadlock/timeout

### Evidence:
- Simple tools work (no Claude calls)
- Direct Python execution works (no nesting)
- Only fails when: Claude → MCP → Claude

## Solution Options

### Option 1: Don't Call Claude from MCP Tools
- Use static content (like original `scrimba_mcp.py`)
- Pre-generate responses
- Works but loses dynamic Claude intelligence

### Option 2: Use Different Architecture
- Have MCP tools return prompts
- Let main Claude process handle generation
- Example:
  ```python
  @mcp.tool()
  async def get_teaching_prompt(topic: str) -> str:
      return f"Teach {topic} using Scrimba methodology..."
  ```

### Option 3: API-Based Approach
- MCP server calls external API
- API server (like `production_api_session.py`) calls Claude
- Avoids subprocess nesting

## Test Code That Works

```python
# simple_test_server.py - WORKS
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-test")

@mcp.tool()
async def test_echo(message: str) -> str:
    return f"Echo: {message}"  # No Claude call - works!

if __name__ == "__main__":
    mcp.run()
```

## Test Code That Fails

```python
# server_claude.py - FAILS
def call_claude(prompt: str) -> str:
    result = subprocess.run([
        "claude", "-p", prompt
    ], ...)  # Subprocess Claude call - deadlocks!
    
@mcp.tool()
async def teach_concept(topic: str) -> str:
    return call_claude(prompt)  # Times out when called via MCP
```

## Verification Commands

```bash
# This works:
claude -p "Use mcp__simple-test__test_echo with message='test'"
# Output: Echo: test

# This times out:
claude -p "Use mcp__scrimba-teaching__teach_concept with topic='variables'"
# Timeout after 30+ seconds
```

## Conclusion

**MCP servers work perfectly with Claude Code** when they:
- Return static/computed responses
- Don't call Claude CLI as subprocess

**MCP servers fail** when they:
- Try to call Claude CLI from within an MCP tool
- Create recursive Claude subprocess calls

## Recommended Approach

For the Scrimba teaching system, use one of:

1. **Static content MCP** (like original `scrimba_mcp.py`)
2. **API-based architecture** (MCP → External API → Claude)
3. **Prompt-returning tools** (let main Claude handle generation)

The current `server_claude.py` architecture (MCP tool calling Claude subprocess) fundamentally cannot work due to process nesting issues.