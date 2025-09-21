#!/usr/bin/env python3
"""
Visual Code Teaching MCP Server
Converts code concepts to visual image prompts
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List

mcp = FastMCP("visual-code")

# Context storage for frame continuity
VISUAL_CONTEXT = {
    "variables": {},
    "scene": "default",
    "frame_count": 0,
    "theme": "pokemon"  # pokemon, racing, cooking
}

# Theme configurations
THEMES = {
    "pokemon": {
        "character": "Ash",
        "item": "Pikachu",
        "scene": "grassy field with trees",
        "container": "Pokeball rack"
    },
    "racing": {
        "character": "Racer",
        "item": "car",
        "scene": "racing track with stands",
        "container": "garage with numbered spots"
    },
    "cooking": {
        "character": "Chef",
        "item": "ingredient",
        "scene": "kitchen with countertop",
        "container": "spice rack with labeled jars"
    }
}

@mcp.tool()
async def variable_visualizer(
    name: str,
    value: str,
    operation: Optional[str] = "assign"
) -> str:
    """
    Visualize variables as quantities of themed items
    """
    theme = THEMES[VISUAL_CONTEXT["theme"]]
    prev_value = VISUAL_CONTEXT["variables"].get(name, 0)
    
    try:
        num_value = int(value)
    except:
        # String or boolean
        return f"Text bubble showing '{name} = {value}' floating above {theme['character']}"
    
    # Update context
    VISUAL_CONTEXT["variables"][name] = num_value
    
    # Generate appropriate prompt based on operation
    if operation == "assign":
        if num_value == 0:
            return f"{theme['scene']} with {theme['character']} standing alone, looking around for {name}"
        elif num_value == 1:
            return f"{theme['scene']} with {theme['character']} and exactly 1 {name} appearing with sparkle effect"
        else:
            return f"{theme['scene']} with {theme['character']} and exactly {num_value} {name}s lined up in a row"
    
    elif operation == "increment":
        diff = num_value - prev_value
        return f"Same scene but now {num_value} {name}s total, the {diff} new one(s) appearing with glow effect"
    
    elif operation == "decrement":
        diff = prev_value - num_value
        return f"Same scene but now only {num_value} {name}s, {diff} fading away with particle effect"
    
    elif operation == "add":
        return f"Visual addition: {prev_value} {name}s + new ones = {num_value} total, shown merging together"

@mcp.tool()
async def comparison_visualizer(
    left: str,
    operator: str,
    right: str
) -> str:
    """
    Visualize comparisons as spatial relationships
    """
    theme = THEMES[VISUAL_CONTEXT["theme"]]
    
    if VISUAL_CONTEXT["theme"] == "racing":
        if operator == ">":
            return f"Split screen racing track: {left} car significantly ahead of {right} car"
        elif operator == "<":
            return f"Split screen racing track: {left} car behind {right} car"
        elif operator == "==":
            return f"Split screen racing track: {left} and {right} cars exactly side-by-side at same position"
        elif operator == ">=":
            return f"Split screen racing track: {left} car ahead or tied with {right} car"
    else:
        # Generic comparison
        if operator == ">":
            return f"Balance scale visualization: {left} (heavier/larger) outweighing {right}"
        elif operator == "<":
            return f"Balance scale visualization: {left} (lighter/smaller) than {right}"
        elif operator == "==":
            return f"Balance scale perfectly balanced: {left} equals {right}"

@mcp.tool()
async def array_visualizer(
    array_name: str,
    operation: str,
    index: Optional[int] = None,
    value: Optional[str] = None
) -> str:
    """
    Visualize arrays as containers with indexed slots
    """
    theme = THEMES[VISUAL_CONTEXT["theme"]]
    
    if operation == "create":
        return f"{theme['container']} with empty numbered slots from 0 to {value or 'several'}"
    
    elif operation == "assign" and index is not None:
        return f"{theme['container']} with slot [{index}] glowing, {value} being placed inside"
    
    elif operation == "push":
        return f"{theme['container']} with new slot appearing at the end, {value} sliding in with motion blur"
    
    elif operation == "pop":
        return f"Last item in {theme['container']} popping out with spring animation, slot disappearing"
    
    elif operation == "access" and index is not None:
        return f"{theme['container']} with slot [{index}] highlighted in golden glow, item inside magnified"
    
    elif operation == "length":
        return f"Overhead view of {theme['container']} with number counter showing total slots"

@mcp.tool()
async def function_sequencer(
    function_name: str,
    steps: List[str]
) -> str:
    """
    Visualize functions as sequential frames
    """
    theme = THEMES[VISUAL_CONTEXT["theme"]]
    
    frames = []
    for i, step in enumerate(steps, 1):
        frames.append(f"Frame {i}: {step}")
    
    prompt = f"**Function: {function_name}**\n"
    prompt += f"Setting: {theme['scene']}\n\n"
    prompt += "Sequential storyboard panels:\n"
    prompt += "\n".join(frames)
    prompt += f"\n\nEach frame shows progression, maintaining same {theme['character']} and setting"
    
    return prompt

@mcp.tool()
async def object_visualizer(
    object_name: str,
    properties: Dict[str, str]
) -> str:
    """
    Visualize objects as entities with highlighted properties
    """
    if VISUAL_CONTEXT["theme"] == "racing":
        # Car example
        frames = []
        for prop, value in properties.items():
            if prop == "wheels":
                frames.append(f"Close-up: {value} wheels glowing with label '{prop}: {value}'")
            elif prop == "engine":
                frames.append(f"Hood open showing {value} engine with label '{prop}: {value}'")
            elif prop == "color":
                frames.append(f"Car body in {value} with shimmer effect, label '{prop}: {value}'")
            else:
                frames.append(f"Dashboard display showing '{prop}: {value}'")
        
        frames.append(f"Final frame: Complete car with all properties labeled around it")
        return "\n".join(frames)
    else:
        # Generic object
        return f"Central {object_name} with properties as labeled bubbles:\n" + \
               "\n".join([f"• {k}: {v} (highlighted)" for k, v in properties.items()])

@mcp.tool()
async def loop_animator(
    loop_type: str,
    iterations: int,
    operations: List[str]
) -> str:
    """
    Visualize loops as transformative sequences
    """
    theme = THEMES[VISUAL_CONTEXT["theme"]]
    
    frames = []
    for i in range(iterations):
        frame_ops = operations[i % len(operations)] if operations else f"iteration {i}"
        frames.append(f"Frame {i+1}: Counter shows '{i}', {frame_ops}")
    
    frames.append(f"Final frame: Loop complete, showing accumulated result")
    
    prompt = f"**Loop Animation ({loop_type})**\n"
    prompt += f"Setting: {theme['scene']}\n\n"
    prompt += "Progressive transformation:\n"
    prompt += "\n".join(frames)
    prompt += "\n\nEach iteration builds on previous, not just repeating"
    
    return prompt

@mcp.tool()
async def set_theme(theme: str) -> str:
    """
    Switch visual theme
    """
    if theme in THEMES:
        VISUAL_CONTEXT["theme"] = theme
        VISUAL_CONTEXT["scene"] = THEMES[theme]["scene"]
        return f"Visual theme switched to: {theme}"
    return f"Unknown theme. Available: {', '.join(THEMES.keys())}"

@mcp.tool()
async def get_context() -> str:
    """
    Get current visual context
    """
    return f"""Current Visual Context:
Theme: {VISUAL_CONTEXT['theme']}
Scene: {VISUAL_CONTEXT['scene']}
Variables: {VISUAL_CONTEXT['variables']}
Frame Count: {VISUAL_CONTEXT['frame_count']}"""

if __name__ == "__main__":
    mcp.run()