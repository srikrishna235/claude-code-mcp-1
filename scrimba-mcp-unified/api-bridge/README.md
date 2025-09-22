# Scrimba Teaching API Bridge

Connect ANY application to Scrimba's revolutionary teaching methodology via simple REST API.

## What This Does

Bridges the gap between:
- **MCP Servers** (designed for Claude CLI)
- **Traditional Apps** (React, Vue, Mobile apps)

## Architecture

```
Your App (React/Mobile)
        ↓ HTTP
    API Bridge
        ↓ JSON-RPC
    MCP Server
        ↓ (optional)
    Claude CLI + Agents
```

## Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn scrimba-teaching-mcp
```

### 2. Start API Server
```bash
cd api-bridge
python api_server.py
```

### 3. Open React Example
```bash
# In another terminal
open examples/react-app.html
```

## API Endpoints

### Core Teaching

**POST /api/teach**
```json
{
  "topic": "variables",
  "step": 1
}
```

**POST /api/challenge**
```json
{
  "difficulty": "easy"
}
```

**POST /api/check**
```json
{
  "code": "let myAge = 25"
}
```

**GET /api/progress**
Returns user's learning progress

## How It Works

### Simple Requests (Direct MCP)
1. HTTP request arrives
2. API spawns/reuses MCP subprocess
3. Sends JSON-RPC command via stdin
4. MCP server processes
5. Returns result via stdout
6. API converts to JSON response

### Complex Requests (With Agents)
1. HTTP request with complex query
2. API detects need for agent
3. Spawns Claude CLI with agent
4. Agent orchestrates multiple tools
5. Returns comprehensive response

## React Integration Example

```javascript
// Teach a concept
fetch('http://localhost:8000/api/teach', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({topic: 'functions'})
})
.then(res => res.json())
.then(data => {
  console.log(data.lesson);
  // Start 60-second timer
  startTimer(data.metadata.time_to_code_seconds);
});
```

## Progressive Enhancement Phases

**✅ Phase 1: Basic Bridge** (DONE)
- MCP subprocess management
- JSON-RPC protocol
- Core endpoints

**✅ Phase 2: Agent Integration** (DONE)
- Claude CLI bridge
- Intelligent routing
- Complex task handling

**📍 Phase 3: Sessions** (Next)
- User tracking
- Progress persistence
- Multi-user support

**Phase 4: WebSocket**
- Real-time updates
- Live coding sessions
- Instant feedback

**Phase 5: Analytics**
- Learning metrics
- Completion tracking
- Performance data

## Testing

### Manual Test
```bash
# Start server
python api_server.py

# Test endpoint
curl -X POST http://localhost:8000/api/teach \
  -H "Content-Type: application/json" \
  -d '{"topic": "variables"}'
```

### React App Test
1. Start API server
2. Open `examples/react-app.html`
3. Click "Teach Variables"
4. Write code when prompted
5. Click "Check My Code"

## Architecture Benefits

**For MCP Servers:**
- No modifications needed
- Works with existing servers
- Maintains protocol compliance

**For Traditional Apps:**
- Simple REST API
- No MCP knowledge needed
- Language agnostic

**For Scale:**
- Stateless API
- Horizontal scaling ready
- Cloud deployment friendly

## Deployment

### Local Development
```bash
python api_server.py
```

### Production (Docker)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "api_server.py"]
```

### Cloud (Heroku/Railway)
```yaml
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python api_server.py"
  }
}
```

## API Documentation

Interactive docs available at:
```
http://localhost:8000/docs
```

## Support Matrix

**Works With:**
- React ✅
- Vue ✅
- Angular ✅
- React Native ✅
- Flutter ✅
- Any HTTP client ✅

**Requires:**
- Python 3.8+
- scrimba-teaching-mcp installed
- (Optional) Claude CLI for agents

## Common Issues

**MCP server won't start**
- Check: `pip install scrimba-teaching-mcp`
- Verify: `python -m scrimba_teaching_mcp` works

**CORS errors**
- API includes CORS headers
- Check browser console
- Try different port if needed

**Timeout errors**
- MCP server may be slow to start first time
- Increase timeout in mcp_bridge.py

## Next Steps

1. **Try the React example** - See it work
2. **Build your integration** - Use any framework
3. **Deploy to cloud** - Scale as needed

---

Built following Progressive Enhancement methodology - works today, better tomorrow.