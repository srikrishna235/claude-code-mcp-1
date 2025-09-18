# Real-time Streaming Solution for Claude CLI via MCP

## Summary
We successfully enabled real-time streaming of Claude CLI output through MCP server by removing the misleading `--output-format stream-json` flag and reading natural language output directly.

## The Problem
- Claude CLI's `--output-format stream-json --verbose` doesn't actually stream
- It buffers all output and dumps it at the end
- This blocked real-time updates despite correct MCP/SSE infrastructure

## The Solution

### Key Changes Made

1. **Removed fake streaming flags**
   ```python
   # Before (doesn't actually stream):
   cmd = [CLAUDE_CLI_PATH, "-p", prompt, "--output-format", "stream-json", "--verbose"]
   
   # After (real interactive mode):
   cmd = [CLAUDE_CLI_PATH, prompt]
   ```

2. **Read stdout directly without JSON parsing**
   ```python
   # Read each line and send immediately
   while True:
       line = await process.stdout.readline()
       if not line:
           break
       line_text = line.decode('utf-8').strip()
       if line_text:
           await context.info(line_text)  # Becomes SSE event
           output_buffer.append(line_text)
   ```

3. **Context notifications automatically become SSE**
   - `context.info()` → LoggingMessageNotification → SSE event
   - No manual SSE formatting needed
   - FastMCP handles the conversion

## Architecture That Works

```
Browser (http://127.0.0.1:8081)
    ↓ POST with Accept: text/event-stream
CORS Proxy (:8001) [async, non-buffering]
    ↓ Forwards immediately
MCP Server (:8000) [mcp_realtime.py]
    ↓ Tool executes with Context
Claude CLI (interactive mode)
    ↓ Outputs to stdout line-by-line
Read each line → context.info()
    ↓ Becomes SSE event
SSE stream back through same POST response
    ↓
Browser receives real-time updates
```

## Why It Works Now

1. **Interactive mode outputs progressively** - Without `-p` flag, Claude shows progress
2. **Stdout has real content** - Not stderr as initially thought
3. **Line-by-line reading** - Using `readline()` not waiting for complete output
4. **Context → SSE pipeline works** - FastMCP automatically converts notifications
5. **Async CORS proxy** - Doesn't buffer, forwards chunks immediately

## Testing Instructions

1. **Servers running:**
   - MCP server: Port 8000 (`mcp_realtime.py`)
   - CORS proxy: Port 8001 (`cors_proxy_async.py`)
   - Terminal UI: Port 8081 (`serve_streaming.py`)

2. **Open browser:** http://127.0.0.1:8081

3. **Test commands:**
   - Simple: `echo "Hello streaming world"`
   - Multi-step: `Create a Python file that prints 1-5 and run it`
   - Complex: `Create and execute a JavaScript file that calculates fibonacci`

## What You Should See

Real-time updates appearing as Claude processes:
- Each line of output appears immediately
- No waiting for complete execution
- Natural language progress messages
- Final result at the end

## Files Modified

1. **mcp_realtime.py**
   - Removed `--output-format stream-json --verbose` flags
   - Removed `-p` flag for interactive mode
   - Simplified to read stdout directly
   - Removed JSON parsing logic

2. **terminal_streaming.html**
   - Fixed to handle SSE from POST response
   - Removed separate EventSource attempt
   - Properly parses SSE events

3. **cors_proxy_async.py**
   - Uses aiohttp for true async streaming
   - Calls `drain()` after each chunk
   - Prevents buffering with headers

## Key Learnings

1. **Tool flags can be misleading** - "stream-json" doesn't mean streaming
2. **Interactive mode is key** - Without `-p`, Claude shows real progress
3. **Context methods work** - They become SSE automatically with streamable-http
4. **Proxy must be async** - Flask/requests buffer, killing real-time
5. **SSE via POST works** - Don't need separate EventSource

## Verification Checklist

✅ Removed misleading flags  
✅ Reading stdout line-by-line  
✅ Context.info() sending each line  
✅ SSE events flowing through proxy  
✅ Browser receiving real-time updates  
✅ Final output still complete  

## Next Steps

For even better streaming:
1. Parse specific progress patterns from Claude's output
2. Add visual progress bars for known operations
3. Implement cancellation support
4. Add buffering for very fast output

---

*Solution implemented: 2024-01-18*  
*Time to solution: 4 hours*  
*Key insight: The tool's own flags were the bottleneck*