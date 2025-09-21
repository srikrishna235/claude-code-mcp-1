# Project Configuration

## Default Agent
All requests in this project should be routed through the orchestrator first.

DEFAULT_AGENT: agent-orchestrator

## Routing Logic
- The `agent-orchestrator` analyzes ALL requests
- Routes educational/visual requests to appropriate specialized agents
- Uses Task tool for proper isolation (prevents multi-tool bleeding)

## Available Specialized Agents
- `scrimba-visual`: Visual learning materials (image prompts only)
- `scrimba-teacher`: Interactive programming lessons