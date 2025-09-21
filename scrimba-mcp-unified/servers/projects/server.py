#!/usr/bin/env python3
"""
Projects MCP Server
Real-world project guidance
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("scrimba-projects")

PROJECTS = {
    "passenger_counter": {
        "name": "Passenger Counter App",
        "story": "My subway counting problem - solved with code!",
        "starter": """let count = 0;

function increment() {
    count = count + 1;
    console.log(count);
}

// Next: Add save() and reset()"""
    },
    "blackjack": {
        "name": "Blackjack Game",
        "story": "I won 100 euros in Prague!",
        "starter": """let firstCard = 10;
let secondCard = 4;
let sum = firstCard + secondCard;"""
    }
}

@mcp.tool()
async def start_project(project_name: Optional[str] = "passenger_counter") -> str:
    """Start a Scrimba project"""
    project = PROJECTS.get(project_name, PROJECTS["passenger_counter"])
    
    return f"""🔨 **PROJECT: {project['name']}**

**Story:** {project['story']}

**Starter Code:**
```javascript
{project['starter']}
```

Start typing NOW! 🚀"""

@mcp.tool()
async def track_progress() -> str:
    """Track project progress"""
    return "📊 Project tracking active!"

if __name__ == "__main__":
    mcp.run()