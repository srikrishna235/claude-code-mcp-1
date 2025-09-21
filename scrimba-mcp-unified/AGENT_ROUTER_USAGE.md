# scrimba_agent - Unified Agent Router Tool

## Overview
Version 1.1.0 introduces `scrimba_agent` - a unified tool that embeds all agent personalities directly in the MCP server.

## Usage Examples

### Auto-Mode (Default)
```python
# Automatically detects intent
scrimba_agent("teach me variables")  # → Interactive lesson
scrimba_agent("show me loops visually")  # → Visual prompt
scrimba_agent("let's build something")  # → Project mode
scrimba_agent("give me a challenge")  # → Challenge mode
```

### Explicit Mode
```python
scrimba_agent("explain arrays", mode="visual")
scrimba_agent("help me learn", mode="interactive")
scrimba_agent("start coding", mode="project")
scrimba_agent("test my skills", mode="challenge")
scrimba_agent("how does this work", mode="orchestrate")
```

## Intent Detection Keywords

### Visual Mode
- "visual", "image", "picture", "diagram", "see", "show me"

### Project Mode  
- "project", "build", "app", "real", "passenger", "blackjack"

### Challenge Mode
- "challenge", "practice", "exercise", "try"

### Progress Mode
- "progress", "score", "how am i", "stats"

### Interactive Mode (Default)
- Any other request defaults to interactive teaching

## Architecture Flow

```
User Request
     ↓
scrimba_agent(prompt)
     ↓
Analyze Intent
     ↓
Route to Mode:
├── Visual → Generate image prompts
├── Interactive → Call teach() internally
├── Project → Call start_project() internally
├── Challenge → Call give_challenge() internally
├── Progress → Call show_progress() internally
└── Orchestrate → Explain the system
```

## Benefits

1. **No Separate Agents Needed** - Everything embedded in MCP
2. **Smart Routing** - Automatically detects user intent
3. **Unified Interface** - Single tool for all teaching modes
4. **Backward Compatible** - Original tools still work

## Testing in Claude

```
# Test auto-routing
> scrimba_agent "teach me about variables visually"

# Test explicit mode
> scrimba_agent prompt="explain functions" mode="visual"

# Test orchestrator
> scrimba_agent prompt="how do you work" mode="orchestrate"
```