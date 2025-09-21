# Project Configuration

## Default Agent
All requests should be routed through the orchestrator first.

DEFAULT_AGENT: orchestrator

## Architecture
- **Agents**: Specialized personalities in `.claude/agents/`
- **MCP Servers**: Separate tools in `servers/`
- **Orchestrator**: Routes requests to appropriate agents
- **Task Tool**: Provides isolation between agents

## Available Agents
- `orchestrator`: Main router (mandatory entry point)
- `teaching`: Interactive Scrimba lessons
- `visual`: Visual learning prompts
- `visual-code`: Code visualization
- `projects`: Real-world projects