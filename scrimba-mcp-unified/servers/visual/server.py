#!/usr/bin/env python3
"""
Visual Learning MCP Server
Generates image prompts for visual learning
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("scrimba-visual")

# Visual prompt templates
VISUAL_PROMPTS = {
    "variables": """
A glowing neon storage box floating in cyberspace, labeled 'count = 0',
with smaller boxes showing count++, count += 5, visual transformation sequence.
Style: Cyberpunk educational, neon blues and purples on dark background,
Matrix-style digital rain, floating code snippets
""",
    "functions": """
A steampunk factory machine with input funnel labeled 'parameters',
internal gears processing, output pipe labeled 'return',
code blocks being transformed.
Style: Industrial educational, brass and copper tones,
steam effects, blueprint aesthetic
""",
    "loops": """
A mesmerizing circular conveyor belt with code blocks repeating,
counter display showing i=0, i<10, i++, items transforming at each cycle.
Style: Futuristic assembly line, glowing holographic displays,
motion blur effects showing repetition
""",
    "arrays": """
A futuristic shelf system with numbered compartments [0][1][2][3],
each containing glowing data orbs, push/pop animations visible.
Style: Sci-fi storage facility, neon indexed labels,
particle effects for data movement
""",
    "objects": """
A magical treasure chest opening to reveal key:value pairs as
floating holographic cards, properties connected by energy beams.
Style: Fantasy RPG interface, glowing magical effects,
enchanted item visualization
""",
    "conditionals": """
A branching pathway in a digital forest, if/else gates glowing,
true path in green, false path in red, decision points highlighted.
Style: Choose-your-own-adventure visualization,
logic gates as mystical portals
"""
}

@mcp.tool()
async def visualize_concept(
    concept: str,
    style: Optional[str] = "scrimba"
) -> str:
    """Generate visual learning prompt for a concept"""
    
    concept_lower = concept.lower()
    
    # Find matching concept
    prompt = VISUAL_PROMPTS.get(concept_lower, VISUAL_PROMPTS["variables"])
    
    return f"""🎨 **VISUAL LEARNING**

**Concept:** {concept.capitalize()}

**Image Generation Prompt:**
```
{prompt}

Additional style: {style}
Resolution: 8K, ultra detailed
Mood: Educational, engaging, memorable
```

**Why This Visual?**
This image creates a PERMANENT mental model of {concept}!
Your brain processes images 60,000x faster than text.

**Learning Path:**
1. Generate this image
2. Stare for 30 seconds
3. Code the concept
4. Never forget it!

Visual + Coding = MASTERY! 🚀"""

@mcp.tool()
async def animate_concept(
    concept: str,
    steps: Optional[int] = 3
) -> str:
    """Generate animation sequence for concept"""
    
    frames = []
    for i in range(1, steps + 1):
        frames.append(f"Frame {i}: Progressive transformation showing step {i}")
    
    return f"""🎬 **ANIMATION SEQUENCE**

**Concept:** {concept}

**Frames:**
{chr(10).join(frames)}

**Animation Instructions:**
- Smooth transitions between frames
- Highlight changes with glow effects
- Maintain consistent visual theme

Each frame builds understanding! 🎯"""

@mcp.tool()
async def visual_challenge(
    difficulty: Optional[str] = "easy"
) -> str:
    """Create visual programming challenge"""
    
    challenges = {
        "easy": "Visualize a variable changing from 0 to 10",
        "medium": "Visualize a function processing input to output",
        "hard": "Visualize a recursive function call stack"
    }
    
    return f"""🎨 **VISUAL CHALLENGE**

**Difficulty:** {difficulty.upper()}

**Your Mission:**
Draw or imagine: {challenges.get(difficulty, challenges["easy"])}

**Success Criteria:**
- Clear visual metaphor
- Shows data flow
- Memorable imagery

Visualize it, then CODE it! 💪"""

@mcp.tool()
async def explain_with_diagram(
    code: str,
    style: Optional[str] = "flowchart"
) -> str:
    """Generate diagram prompt to explain code"""
    
    return f"""📊 **CODE VISUALIZATION**

**Your Code:**
```javascript
{code}
```

**Diagram Prompt:**
Create a {style} showing:
- Data flow from start to finish
- Each operation as a visual step
- Variables as containers
- Functions as processors

**Visual Style:**
- Clean, educational design
- Color-coded by operation type
- Arrows showing flow direction

This diagram will make your code crystal clear! 🎯"""

@mcp.tool()
async def create_meme(
    programming_topic: str,
    mood: Optional[str] = "encouraging"
) -> str:
    """Generate programming meme for fun learning"""
    
    return f"""😄 **PROGRAMMING MEME**

**Topic:** {programming_topic}
**Mood:** {mood}

**Meme Prompt:**
Drake meme format:
- Top (rejecting): "Reading 500 pages of documentation"
- Bottom (approving): "Learning {programming_topic} by writing code immediately"

Style: Relatable programmer humor, encouraging tone

Laugh and learn! That's the Scrimba way! 🚀"""

if __name__ == "__main__":
    mcp.run()