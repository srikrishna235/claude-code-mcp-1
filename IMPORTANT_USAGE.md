# ⚠️ IMPORTANT: How to Use Claude Code Terminal

## DO NOT open terminal.html directly in your browser!

❌ **WRONG**: Opening the file directly (file:///home/rishabh/Desktop/dev/claude-code-mcp/terminal.html)
   - This will NOT work due to browser security (CORS)
   - You'll get "Connection Failed" errors

✅ **CORRECT**: Access through the HTTP server
   
   1. Run the start script:
   ```bash
   ./start_all.sh
   ```
   
   2. Open your browser at:
   ```
   http://127.0.0.1:8080
   ```
   
   NOT the file path, but the HTTP URL!

## Why This Matters

Browsers block file:// URLs from making HTTP requests for security reasons. The terminal MUST be accessed through the HTTP server (port 8080) to communicate with the MCP server (port 8005).

## Quick Test

After starting the servers, open:
- http://127.0.0.1:8080 (Terminal interface)
- You should see "Connected" with a green dot
- Try typing: "What is 2 + 2?"

If you see the terminal at file:/// in your address bar, you're doing it wrong!