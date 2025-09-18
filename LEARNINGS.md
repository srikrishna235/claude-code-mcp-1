# Core Learnings: MCP + Claude CLI Streaming Implementation

## Executive Summary
We attempted to implement real-time streaming of Claude CLI output through an MCP (Model Context Protocol) server. This document captures critical learnings about MCP, SSE streaming, and the realities of subprocess communication.

---

## 1. MCP Architecture Insights

### How MCP Actually Works
- **MCP is a protocol**, not just an API wrapper
- Uses JSON-RPC 2.0 for message passing
- Supports multiple transports: stdio, SSE (streamable-http), WebSocket

### Key Components
```
FastMCP Server
    ↓
Session Manager (handles connections)
    ↓
Tools (decorated functions)
    ↓
Context (for notifications)
```

### Critical Discovery: Streamable-HTTP Transport
- **Single POST request can return SSE stream**
- Client sends: `Accept: application/json, text/event-stream`
- Server responds with SSE if it has notifications to send
- **NOT** a separate EventSource connection

---

## 2. SSE (Server-Sent Events) Realities

### What We Thought
- Need separate EventSource connection for notifications
- POST for commands, GET for SSE stream
- Two-channel architecture

### What Actually Happens
- **Single channel**: POST request itself becomes SSE stream
- When Accept includes `text/event-stream`, response streams
- Notifications interleaved with final result

### EventSource Limitations
- **Cannot send custom headers** (major limitation)
- Cannot send session ID or authentication
- This is why MCP uses POST for SSE, not GET with EventSource

---

## 3. Context Notifications vs Direct Streaming

### Context Methods Work...With Caveats
```python
await ctx.info("message")         # → LoggingMessageNotification
await ctx.report_progress(50, 100) # → ProgressNotification
```

**These DO become SSE events** when using streamable-http transport:
```
event: message
data: {"method": "notifications/message", "params": {...}}
```

### But Context Doesn't Capture External Process Output
- Context sends MCP protocol messages
- External subprocess output is separate
- Need to manually bridge: read subprocess → call Context method

---

## 4. Claude CLI Behavior Discoveries

### The Streaming Illusion
**Critical Learning**: `--output-format stream-json` doesn't actually stream!
- Buffers all events internally
- Outputs everything at once when complete
- The "stream" is a lie - it's batch output formatted as events

### Flag Impacts
```bash
claude -p "prompt"                    # Print mode, no interaction
claude "prompt"                        # Interactive mode
--output-format stream-json --verbose # Requires both flags together
--dangerously-skip-permissions        # Bypasses approval prompts
```

### Where Real Progress Lives
- **stderr** contains real-time progress (not stdout)
- Interactive mode shows more progress
- JSON output mode suppresses natural progress

---

## 5. CORS Proxy Requirements

### Flask vs Async Solutions
**Flask with requests library**: Buffers entire response
```python
Response(generate())  # Still buffers, doesn't truly stream
```

**aiohttp/FastAPI**: Can truly stream
```python
async for chunk in response.content.iter_any():
    await response.write(chunk)
    await response.drain()  # Force flush
```

### Critical Headers for SSE
```
Content-Type: text/event-stream
Cache-Control: no-cache
X-Accel-Buffering: no  # Disable nginx buffering
Connection: keep-alive
```

---

## 6. The Real Architecture That Works

### Successful Pattern
```
Browser
    ↓ (fetch with Accept: SSE)
CORS Proxy (async, non-buffering)
    ↓ (forwards immediately)
MCP Server (FastMCP)
    ↓ (creates Context)
Tool Function
    ↓ (spawns subprocess)
Claude CLI
    ↓ (outputs to stdout/stderr)
Parse Output
    ↓ (line by line)
Context.info() / report_progress()
    ↓ (becomes SSE events)
SSE Stream
    ↓ (through same POST response)
Browser receives progressive updates
```

---

## 7. Common Pitfalls We Hit

### Pitfall 1: Expecting EventSource to Work
- EventSource can't send headers
- MCP needs session ID in headers
- Solution: POST request that returns SSE

### Pitfall 2: Trusting --output-format stream-json
- Name suggests streaming, but doesn't
- Actually buffers everything
- Solution: Parse regular output or stderr

### Pitfall 3: Using subprocess.run()
- Blocks until complete
- Can't read output progressively
- Solution: asyncio.create_subprocess_exec()

### Pitfall 4: Wrong Accept Headers
- `Accept: application/json` → No streaming
- `Accept: text/event-stream` → No structured response
- `Accept: application/json, text/event-stream` → Both work

### Pitfall 5: CORS Proxy Buffering
- Flask/requests buffer by default
- Kills real-time streaming
- Solution: Async frameworks with explicit flushing

---

## 8. What Actually Enables Streaming

### Required Conditions (ALL must be true)
1. ✅ Async subprocess execution
2. ✅ Line-by-line output reading
3. ✅ Context notifications in tool
4. ✅ Streamable-http transport
5. ✅ Non-buffering proxy
6. ✅ Correct Accept headers
7. ❌ Claude CLI actually streaming (this was our blocker)

### The Final Blocker
Claude CLI itself doesn't stream with current flags. Options:
1. Remove flags, parse natural output
2. Use interactive mode
3. Read stderr for progress
4. Build native Python implementation

---

## 9. Simplified Working Implementation

### Minimal Viable Streaming
```python
@mcp.tool()
async def execute(prompt: str, ctx: Context) -> str:
    # Start process WITHOUT special flags
    proc = await asyncio.create_subprocess_exec(
        'claude', prompt,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Stream stderr (where progress appears)
    async for line in proc.stderr:
        text = line.decode().strip()
        if text:
            await ctx.info(text)  # Becomes SSE event
    
    return "Complete"
```

---

## 10. Key Takeaways

### Technical Lessons
1. **Read the source, not just docs** - Implementation details matter
2. **Test each layer independently** - Isolate where streaming breaks
3. **Command-line flags can lie** - "stream-json" doesn't mean streaming
4. **SSE is simpler than WebSockets** - But has limitations (no headers)
5. **Context is powerful** - When used with right transport

### Architectural Lessons
1. **Progressive enhancement works** - We got intermediate steps working first
2. **Don't over-engineer** - EventSource seemed right but wasn't needed
3. **Proxies can break streaming** - Choose carefully
4. **Subprocess output is complex** - stdout vs stderr, buffering, etc.

### Process Lessons
1. **Small tests reveal truth** - `curl` tests showed SSE format quickly
2. **Browser DevTools are essential** - Network tab shows real headers
3. **Logging at each layer** - Helped identify where streaming stopped
4. **Binary search debugging** - Systematically narrowed down the issue

---

## 11. Future Improvements

### Short Term
- Remove `--output-format stream-json` flag
- Parse Claude's natural output
- Use stderr for real progress

### Medium Term
- Build native Python tool implementation
- Skip Claude CLI entirely for simple tasks
- Use CLI only for complex operations

### Long Term
- Contribute to FastMCP for better streaming docs
- Build proper SSE testing tools
- Create streaming subprocess wrapper library

---

## Conclusion

The journey revealed that "streaming" has many layers:
1. Network streaming (SSE)
2. Protocol streaming (MCP notifications)  
3. Process streaming (subprocess output)
4. Application streaming (Claude CLI behavior)

Success requires ALL layers to cooperate. Our implementation was correct at layers 1-3, but layer 4 (Claude CLI) wasn't actually streaming despite its flags suggesting otherwise.

The core learning: **Always verify assumptions at each layer of the stack.**

---

*Generated from debugging session on 2024-01-18*
*Total time invested: ~4 hours*
*Lines of code written: ~2500*
*Key insight discovered at: Hour 3.5*