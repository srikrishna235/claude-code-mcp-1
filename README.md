# Claude Code MCP Server

Exposes Claude Code CLI's AI capabilities as an MCP (Model Context Protocol) server.

## What This Is

This server wraps the actual Claude Code CLI (`claude` command) to expose its AI-powered coding capabilities via MCP protocol. Claude Code is an AI coding assistant that understands natural language and can read, write, edit code, run commands, and more.

## Architecture

```
MCP Client (e.g., Claude Desktop)
    ↓ HTTP (Streamable HTTP Transport)
MCP Server (claude_code_mcp_final.py)
    ↓ Subprocess call
Claude Code CLI (AI-powered)
    ↓ Uses built-in tools
File System/Terminal
```

## How It Works

1. **MCP Client** sends natural language prompt (e.g., "Fix the bug in server.py")
2. **MCP Server** passes prompt to Claude Code CLI via `claude -p`
3. **Claude Code AI** analyzes, plans, and executes using its tools
4. **Response** returns through MCP protocol

## Quick Start

### 1. Prerequisites

Install Claude Code CLI:
```bash
npm install -g @anthropic-ai/claude-code
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Server

```bash
python claude_code_mcp_final.py
```

The server runs on `http://127.0.0.1:8000/mcp`

### 3. Configure Claude Desktop

Add to `~/.claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "claude-code": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

### 4. Restart Claude Desktop

The server will appear in Claude Desktop's MCP servers list.

## Usage Examples

Once connected, you can ask Claude Desktop to use Claude Code for tasks like:

- "What does this project do?"
- "Fix the TypeScript errors in src/index.ts"
- "Add error handling to the database connection"
- "Create a REST API for user management"
- "Refactor this function to be more readable"

## Available Tool

- **claude_execute**: Executes natural language tasks using Claude Code CLI
  - `prompt`: Task description in natural language
  - `working_dir`: Optional working directory
  - `allowed_tools`: Optional list of allowed Claude Code tools

## Implementation

- **Single file**: `claude_code_mcp_final.py` (~120 lines)
- **Transport**: Streamable HTTP (production-ready)
- **Dependency**: Requires Claude Code CLI installed

## Future Enhancements

- Phase 2: Add specialized tools for common tasks
- Phase 3: Add resources for file browsing
- Phase 4: Add prompts for workflows
- Phase 5: Add streaming support

Total implementation: ~120 lines
Following Progressive Enhancement methodology