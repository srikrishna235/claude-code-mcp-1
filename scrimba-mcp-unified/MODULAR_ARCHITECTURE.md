# Modular Architecture v2.0

## Structure
```
scrimba-mcp-unified/
├── .claude/agents/          # Agent personalities
│   ├── orchestrator.md     # Routes all requests
│   ├── teaching.md         # Scrimba teaching
│   ├── visual.md           # Visual prompts
│   ├── visual-code.md      # Code visualization
│   └── image-gen.md        # Image generation
│
├── servers/                # Separate MCP servers
│   ├── teaching/          # Core teaching tools
│   │   └── server.py      # teach, challenge, check_code
│   ├── visual/            # Visual learning
│   │   └── server.py      # visualize_concept, animate
│   ├── visual-code/       # Code visualization
│   │   └── server.py      # variable_visualizer, arrays
│   └── projects/          # Real projects
│       └── server.py      # start_project, track
│
├── .mcp.json              # Configure all servers
└── CLAUDE.md              # Sets orchestrator as default
```

## How It Works

1. **User Request** → Goes to orchestrator (default agent)
2. **Orchestrator** → Analyzes and routes via Task tool
3. **Specific Agent** → Handles with personality
4. **MCP Server** → Provides actual tools
5. **Response** → Back through agent chain

## Benefits

- **Modular**: Each component has single responsibility
- **Maintainable**: Small focused files (<300 lines)
- **Scalable**: Easy to add new agents/servers
- **Isolated**: Task tool prevents bleeding

## Usage

```bash
# In Claude Code with this structure:
cd scrimba-mcp-unified
# Request gets routed automatically through orchestrator
```

This follows the proven claude-code-mcp pattern!