# Claude Code Terminal Interface

A web-based terminal interface for interacting with Claude Code via MCP protocol.

## Features

- 🖥️ **Terminal-like UI**: Dark theme, monospace font, familiar terminal aesthetics
- 💬 **Natural Language**: Type commands in plain English
- 🤖 **AI-Powered**: Uses Claude Code's AI capabilities
- 🔄 **Real-time**: Live connection status and responses
- 📁 **File Operations**: Read, write, edit files using Claude's intelligence
- 🎨 **Syntax Highlighting**: Code blocks are properly formatted

## Quick Start

### Automatic Start (Recommended)
```bash
./start_all.sh
```
This starts both servers and opens the terminal at http://127.0.0.1:8080

### Manual Start
```bash
# Terminal 1: Start MCP server
python claude_code_mcp_final.py --port 8005

# Terminal 2: Start Terminal server
python terminal_server.py --port 8080

# Open browser at http://127.0.0.1:8080
```

## Usage Examples

Type natural language commands in the terminal:

### Code Analysis
- "What does this project do?"
- "Explain the main.py file"
- "Find all TODO comments in the codebase"

### Code Modification
- "Add error handling to the calculate function"
- "Fix the bug in server.py line 42"
- "Add docstrings to all functions in utils.py"

### Code Creation
- "Create a REST API endpoint for user management"
- "Write a function to validate email addresses"
- "Implement a binary search algorithm"

### General Queries
- "What is 15 + 27?"
- "How do I use async/await in Python?"
- "What's the difference between let and const?"

## How It Works

```
Terminal (Browser)
    ↓ HTTP + JSON-RPC
MCP Server (Port 8005)
    ↓ Subprocess
Claude Code CLI
    ↓ AI Processing
File System
```

1. **User Input**: Type command in terminal
2. **MCP Protocol**: Sent via JSON-RPC to MCP server
3. **Claude Code**: Executes using AI capabilities
4. **Response**: Displayed in terminal with formatting

## Interface Controls

- **Enter**: Send command
- **Shift+Enter**: New line in input
- **Clear**: Clear terminal history
- **Status Indicator**: Shows connection status (green = connected)

## Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Backend**: FastMCP server with CORS support
- **Protocol**: Model Context Protocol (MCP)
- **Transport**: HTTP with Server-Sent Events
- **AI Engine**: Claude Code CLI

## Architecture

```
terminal.html         # Web interface
    ↓
terminal_server.py    # Serves HTML, handles CORS
    ↓
claude_code_mcp_final.py  # MCP server wrapper
    ↓
claude CLI            # Actual AI engine
```

## Customization

### Change Ports
Edit `terminal.html`:
```javascript
const MCP_URL = 'http://127.0.0.1:8005/mcp';  // Change port here
```

### Modify Styling
Edit the `<style>` section in `terminal.html` to customize:
- Colors
- Fonts
- Layout
- Animations

## Troubleshooting

### Connection Failed
- Ensure MCP server is running on port 8005
- Check Claude Code CLI is installed: `npm install -g @anthropic-ai/claude-code`
- Verify no firewall blocking ports

### No Response
- Check browser console for errors (F12)
- Verify session is connected (green indicator)
- Try reconnecting by refreshing page

### CORS Issues
- MCP server includes CORS headers
- Terminal server acts as proxy if needed
- Use provided start script for proper setup

## Security Note

This is designed for local development. For production:
- Add authentication
- Use HTTPS
- Restrict CORS origins
- Implement rate limiting

## Future Enhancements

- [ ] Command history (up/down arrows)
- [ ] Tab completion
- [ ] Multiple sessions/tabs
- [ ] File tree browser
- [ ] Syntax highlighting in input
- [ ] Export conversation
- [ ] Themes/customization