#!/usr/bin/env python3
"""
CLI Wrapper MCP Server - Provides Agent Support
Wraps Claude CLI to enable agent-based orchestration
Works alongside the teaching MCP server
"""

import os
import sys
import subprocess
import shutil
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Check if Claude CLI is installed
CLAUDE_CLI_PATH = shutil.which("claude")
if not CLAUDE_CLI_PATH:
    print("Warning: Claude CLI not installed. This wrapper requires Claude CLI for agent support.", file=sys.stderr)
    print("Install with: npm install -g @anthropic-ai/claude-code", file=sys.stderr)
    # Don't exit - let it run anyway for MCP registration

# Initialize MCP server
mcp = FastMCP("claude-cli-wrapper")

@mcp.tool()
async def execute_with_agent(
    prompt: str,
    agent: Optional[str] = None,
    working_dir: Optional[str] = None
) -> str:
    """
    Execute a prompt using Claude CLI with optional agent support.
    This enables the agent orchestration layer on top of MCP tools.
    
    Args:
        prompt: The task or question
        agent: Agent name to use (e.g., "agent-orchestrator")
        working_dir: Working directory for execution
    
    Returns:
        Response from Claude CLI with agent processing
    """
    if not CLAUDE_CLI_PATH:
        return "Claude CLI is not installed. Please install it first."
    
    try:
        # Build command
        if agent:
            cmd = [CLAUDE_CLI_PATH, f"@{agent}", prompt]
        else:
            cmd = [CLAUDE_CLI_PATH, "-p", prompt]
        
        # Add safety flag
        cmd.append("--dangerously-skip-permissions")
        
        # Set working directory
        cwd = os.path.expanduser(working_dir) if working_dir else os.getcwd()
        
        # Execute with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60,
            env=os.environ.copy()
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Request timed out after 60 seconds"
    except Exception as e:
        return f"Error executing Claude CLI: {str(e)}"

@mcp.tool()
async def list_available_agents() -> str:
    """
    List all available agents in the project.
    
    Returns:
        List of available agents with descriptions
    """
    agents_dir = os.path.expanduser("~/.claude/agents")
    project_agents_dir = ".claude/agents"
    
    agents = []
    
    # Check global agents
    if os.path.exists(agents_dir):
        for file in os.listdir(agents_dir):
            if file.endswith(".md"):
                agent_name = file[:-3]
                agents.append(f"Global: @{agent_name}")
    
    # Check project agents
    if os.path.exists(project_agents_dir):
        for file in os.listdir(project_agents_dir):
            if file.endswith(".md"):
                agent_name = file[:-3]
                agents.append(f"Project: @{agent_name}")
    
    if agents:
        return "Available agents:\n" + "\n".join(agents)
    else:
        return "No agents found. Agents should be in ~/.claude/agents/ or .claude/agents/"

@mcp.tool()
async def create_teaching_agent(
    agent_type: str = "orchestrator"
) -> str:
    """
    Create a teaching agent configuration.
    
    Args:
        agent_type: Type of agent (orchestrator, visual, interactive)
    
    Returns:
        Status message about agent creation
    """
    agents_dir = ".claude/agents"
    os.makedirs(agents_dir, exist_ok=True)
    
    agents = {
        "orchestrator": {
            "name": "teaching-orchestrator",
            "content": """---
name: teaching-orchestrator
description: Routes all teaching requests to appropriate MCP tools
tools: mcp__scrimba-teaching__teach, mcp__scrimba-teaching__give_challenge, mcp__scrimba-teaching__check_code
model: sonnet
---

You route teaching requests to the Scrimba Teaching MCP server.

# Routing Rules
- Teaching requests → Use teach() tool
- Challenge requests → Use give_challenge() tool
- Code submissions → Use check_code() tool

Always use the MCP tools. They contain the full Scrimba methodology."""
        },
        "visual": {
            "name": "visual-teacher",
            "content": """---
name: visual-teacher
description: Handles visual learning requests
tools: mcp__scrimba-teaching__visualize_concept
model: sonnet
---

You create visual learning materials using the Scrimba Teaching MCP server.
Always use visualize_concept() for any visual teaching request."""
        }
    }
    
    if agent_type not in agents:
        return f"Unknown agent type. Available: {', '.join(agents.keys())}"
    
    agent = agents[agent_type]
    agent_path = os.path.join(agents_dir, f"{agent['name']}.md")
    
    with open(agent_path, 'w') as f:
        f.write(agent['content'])
    
    return f"Created agent: @{agent['name']} at {agent_path}\nUse: claude @{agent['name']} 'your request'"

# Run the server
if __name__ == "__main__":
    mcp.run()