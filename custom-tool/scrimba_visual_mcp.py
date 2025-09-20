#!/usr/bin/env python3
"""
Scrimba Visual MCP Server - Teaching programming through AI-generated images
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

# Initialize MCP server
mcp = FastMCP("scrimba-visual")

# Track current visual lesson state
CURRENT_VISUAL = {
    "concept": None,
    "step": 1,
}

@mcp.tool()
async def visualize_concept(
    concept: str,
    style: Optional[str] = "scrimba"
) -> str:
    """
    Generate an image prompt to visualize a programming concept.
    
    Args:
        concept: The concept to visualize (e.g., "variables", "loops", "functions")
        style: Visual style (default: "scrimba")
    
    Returns:
        Image generation prompt and explanation
    """
    
    CURRENT_VISUAL["concept"] = concept
    
    prompts = {
        "variables": {
            "prompt": "Create a bright, colorful illustration showing programming variables as labeled storage boxes. Show 3 boxes: one labeled 'name' containing 'Per', one labeled 'age' containing '25', and one labeled 'isTeacher' containing 'true'. Use a clean, minimalist style with vibrant colors (blue, orange, green). Add arrows pointing to each box with 'let' keyword. Background should be light with subtle grid pattern. Style: educational infographic, Scrimba-inspired, beginner-friendly",
            "explanation": "Variables are like **labeled boxes** that store your stuff! Each box has a name and holds a value!"
        },
        "loops": {
            "prompt": "Create an animated-style illustration of a loop concept. Show a circular track with a small robot running around it. Include numbered checkpoints (1, 2, 3) that light up as the robot passes. Add a counter display showing 'Round: 3/5'. Use bright colors (purple track, yellow robot, green checkpoints). Include code snippet 'for(i=0; i<5; i++)' floating above. Style: playful educational diagram, clean vectors, Scrimba teaching style",
            "explanation": "Loops make your code **run in circles** - but in a good way! Do something multiple times without typing it over and over!"
        },
        "functions": {
            "prompt": "Illustrate a function as a magical machine. Show a colorful factory-style machine with input funnel on left labeled 'ingredients', gears in middle labeled 'function bakeCake()', and output conveyor on right with a cake. Use bright, friendly colors (pink machine, blue gears, yellow cake). Add speech bubble saying 'Reusable magic!'. Style: whimsical technical diagram, Scrimba educational, beginner-friendly illustration",
            "explanation": "Functions are **reusable machines** - put ingredients in, get results out! Write once, use everywhere!"
        },
        "arrays": {
            "prompt": "Create an illustration of an array as a colorful train. Each train car is numbered (0, 1, 2, 3) and contains different items (apple, banana, orange, grape). Show 'fruits' as the train name. Include visual index numbers below each car. Use vibrant colors, clean flat design. Add code 'fruits[1]' with arrow pointing to banana car. Style: educational infographic, Scrimba-inspired, programming for beginners",
            "explanation": "Arrays are like **trains with numbered cars** - each car holds something and you can access them by their number!"
        },
        "objects": {
            "prompt": "Visualize a JavaScript object as a colorful backpack with labeled pockets. Main backpack labeled 'student'. Show transparent pockets containing: 'name: Per', 'age: 25', 'skills: [JS, React]'. Use bright colors (orange backpack, blue pockets). Include accessing notation 'student.name' with arrow. Style: flat design educational illustration, Scrimba teaching style, clean and friendly",
            "explanation": "Objects are like **backpacks with labeled pockets** - organize related stuff together!"
        },
        "conditionals": {
            "prompt": "Illustrate if-else as a colorful road fork. Show a character at intersection with two paths: left path (green, sunny) labeled 'if (weather === sunny)' leading to beach, right path (blue, rainy) labeled 'else' leading to indoor cafe. Add decision bubble above character. Use bright, cheerful colors. Style: cartoon educational diagram, Scrimba-inspired decision tree",
            "explanation": "If-else statements are **decision points** - choose which path your code takes based on conditions!"
        }
    }
    
    visual = prompts.get(concept, {
        "prompt": f"Create a bright, educational illustration explaining the programming concept of {concept}. Use simple visual metaphors, bright colors (orange, blue, green), clean minimalist style. Include small code snippets. Style: Scrimba educational, beginner-friendly infographic",
        "explanation": f"Let's visualize {concept} to make it crystal clear!"
    })
    
    return f"""🎨 **VISUAL LEARNING TIME!**

**Image Prompt for AI Generation:**
```
{visual['prompt']}
```

**What This Shows:**
{visual['explanation']}

**Why Visual Learning Works:**
Our brains process images 60,000x faster than text! This image will make {concept} STICK in your mind forever!

Type 'animate_concept' to see this in motion!
Or 'visual_challenge' to test your understanding!"""

@mcp.tool()
async def animate_concept(
    concept: Optional[str] = None,
    steps: Optional[int] = 3
) -> str:
    """
    Generate animation prompts showing concept step-by-step.
    
    Args:
        concept: Concept to animate (uses current if not specified)
        steps: Number of animation frames
    
    Returns:
        Multiple image prompts for animation sequence
    """
    if not concept:
        concept = CURRENT_VISUAL.get("concept", "variables")
    
    animations = {
        "variables": [
            "Show empty workspace with 'let' keyword appearing with sparkle effect. Bright, clean background.",
            "Box materializes next to 'let', gets labeled 'myName'. Box glows and opens showing it's empty.",
            "Value 'Per' flies in with trail effect and lands inside box. Box closes with satisfaction. Show complete: let myName = 'Per'"
        ],
        "loops": [
            "Robot at starting line of circular track. Counter shows '0'. Track segments numbered 1-10.",
            "Robot running on track, passing segments 1-3. They light up green as passed. Counter shows '3'.",
            "Robot completing final lap, all segments lit. Counter shows '10'. Confetti explosion! 'Loop Complete!'"
        ],
        "functions": [
            "Empty workspace. Text appears: 'function greet(name)'. Machine starts assembling piece by piece.",
            "Machine complete. Input funnel receives 'Per'. Gears start turning with colorful animation.",
            "Output conveyor produces 'Hello, Per!' in speech bubble. Machine gives thumbs up. 'Reusable!' badge appears."
        ]
    }
    
    frames = animations.get(concept, [
        f"Frame 1: Setup the {concept} visual with anticipation",
        f"Frame 2: Show the {concept} in action with movement",
        f"Frame 3: Complete the {concept} with celebration"
    ])
    
    return f"""🎬 **ANIMATED LEARNING: {concept.upper()}**

**Animation Sequence ({steps} frames):**

{chr(10).join([f'**Frame {i+1}:**\n```\n{frame}\nStyle: Bright, playful, Scrimba educational animation\n```\n' for i, frame in enumerate(frames[:steps])])}

**Animation Notes:**
- Each frame builds excitement!
- Use smooth transitions between frames
- Keep colors consistent but add motion effects
- Include particle effects for emphasis

This animation will make {concept} IMPOSSIBLE to forget!

Type 'visual_challenge' to test what you learned!"""

@mcp.tool()
async def visual_challenge(
    difficulty: Optional[str] = "easy"
) -> str:
    """
    Create visual programming challenges.
    
    Args:
        difficulty: Challenge level (easy/medium/hard)
    
    Returns:
        Visual challenge with image prompt
    """
    concept = CURRENT_VISUAL.get("concept", "variables")
    
    challenges = {
        "easy": {
            "task": "Look at this image and write the code it represents!",
            "prompt": "Create an image showing 3 labeled boxes: 'score' with value 0, 'lives' with value 3, 'gameOver' with value false. Show these as colorful 3D boxes on a shelf. Include question marks suggesting user should write the code. Style: gamified educational diagram",
            "hint": "Each box needs a 'let' keyword!",
            "solution": "let score = 0;\nlet lives = 3;\nlet gameOver = false;"
        },
        "medium": {
            "task": "This image shows a problem - write code to solve it!",
            "prompt": "Illustrate a visual problem: 5 identical robots in a line looking sad, with thought bubble 'We need unique names!'. Show empty array structure below labeled 'robotNames'. Style: problem-solving educational illustration",
            "hint": "Use a loop to give each robot a unique name!",
            "solution": "let robotNames = [];\nfor(let i = 1; i <= 5; i++) {\n  robotNames.push('Robot' + i);\n}"
        },
        "hard": {
            "task": "Debug this visual representation!",
            "prompt": "Show a broken machine (function) with gears misaligned. Input shows 'Hello' going in, output shows 'ERROR'. Red X marks and steam clouds. One gear labeled 'return' is missing. Style: debugging educational diagram",
            "hint": "The function is missing something important!",
            "solution": "function shout(text) {\n  return text.toUpperCase() + '!';\n  // Was missing the return statement!\n}"
        }
    }
    
    challenge = challenges.get(difficulty, challenges["easy"])
    
    return f"""🎯 **VISUAL CHALLENGE TIME!**

**Difficulty:** {difficulty.upper()}

**Challenge Image Prompt:**
```
{challenge['prompt']}
```

**YOUR MISSION:** {challenge['task']}

**Write your code solution!**
When you're done (or stuck), I'll check it!

💡 Need a hint? Just ask!
First hint: {challenge['hint']}

This visual challenge makes coding feel like solving puzzles!"""

@mcp.tool()
async def explain_with_diagram(
    code: str,
    style: Optional[str] = "flowchart"
) -> str:
    """
    Generate diagram prompt to explain user's code visually.
    
    Args:
        code: The code to visualize
        style: Diagram style (flowchart/memory/execution)
    
    Returns:
        Diagram prompt to explain the code
    """
    # Analyze code to determine what to visualize
    has_loop = "for" in code or "while" in code
    has_function = "function" in code
    has_conditional = "if" in code
    
    if style == "flowchart":
        prompt = f"""Create a colorful flowchart diagram explaining this code:
{code}

Use rounded rectangles for processes (blue), diamonds for decisions (green), ovals for start/end (orange).
Add arrows showing flow direction. Include actual code snippets in each shape.
Style: Clean educational flowchart, Scrimba-inspired, bright colors, beginner-friendly"""
    elif style == "memory":
        prompt = f"""Create a memory diagram showing how variables are stored for this code:
{code}

Show memory as colorful shelves or boxes. Each variable gets its own labeled space.
Show values changing if they're updated. Use arrows to show assignments.
Style: Computer memory visualization, educational, bright and friendly"""
    else:  # execution
        prompt = f"""Create step-by-step execution diagram for this code:
{code}

Show each line executing with highlighting. Display variable values in sidebar.
Use play button icons and step numbers. Show output in console area.
Style: Code execution visualizer, educational debugger view, Scrimba colors"""
    
    return f"""🎨 **YOUR CODE VISUALIZED!**

**Diagram Generation Prompt:**
```
{prompt}
```

**What This Diagram Shows:**
- How your code flows from start to finish
- Where decisions are made
- How data moves through your program
{"- Loop iterations clearly shown" if has_loop else ""}
{"- Function calls and returns" if has_function else ""}
{"- Conditional branches" if has_conditional else ""}

**Why This Helps:**
Seeing your code as a picture makes bugs OBVIOUS!
You'll never forget how this code works!

Want a different view? Try 'memory' or 'execution' style!"""

@mcp.tool()
async def create_meme(
    programming_topic: str,
    mood: Optional[str] = "encouraging"
) -> str:
    """
    Generate programming meme for fun learning.
    
    Args:
        programming_topic: Topic for the meme
        mood: Meme mood (encouraging/relatable/victorious)
    
    Returns:
        Meme image prompt
    """
    memes = {
        "debugging": {
            "encouraging": "Drake meme format: Top (rejecting): 'Giving up when code doesn't work'. Bottom (approving): 'console.log() EVERYTHING'. Style: Bright colors, programming humor",
            "relatable": "Distracted boyfriend meme: Boyfriend labeled 'Me', girlfriend labeled 'My working code', other woman labeled 'Adding just one more feature'. Style: Programming humor",
            "victorious": "Success kid meme: Text top: 'Fixed bug on first try', Text bottom: 'It was a missing semicolon'. Fist pump victory pose. Style: Celebration meme"
        },
        "learning": {
            "encouraging": "Galaxy brain meme: Small brain: 'Copy-paste from Stack Overflow', Medium brain: 'Understanding the code', Galaxy brain: 'Teaching someone else'. Style: Progressive learning",
            "relatable": "This is fine meme: Dog in burning room labeled 'Me', fire labeled 'My code errors', speech: 'I'm learning'. Style: Relatable programming journey",
            "victorious": "Expanding brain meme showing progression: 'Hello World' -> 'First Function' -> 'Built an App'. Style: Learning journey celebration"
        }
    }
    
    topic_memes = memes.get(programming_topic, memes["learning"])
    meme_prompt = topic_memes.get(mood, topic_memes["encouraging"])
    
    return f"""😂 **MEME BREAK!**

**Meme Generation Prompt:**
```
{meme_prompt}
Add text overlays in Impact font.
Make it colorful and positive.
Style: Programming education meme, Scrimba humor, beginner-friendly
```

**Why Memes Help Learning:**
- Humor makes concepts STICK
- Relatable content builds confidence  
- Shared struggles create community

You're not alone in this journey - we ALL went through this!

Share this with fellow learners! 🚀"""

if __name__ == "__main__":
    import sys
    
    if "--http" in sys.argv:
        import asyncio
        import uvicorn
        from starlette.applications import Starlette
        from starlette.middleware.cors import CORSMiddleware
        
        async def run_server():
            app = Starlette()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            mcp_app = mcp.streamable_http_app()
            app.mount("/", mcp_app)
            
            async with mcp.session_manager.run():
                print("Scrimba Visual MCP Server")
                print("=========================")
                print("Tools: visualize_concept, animate_concept, visual_challenge")
                print("       explain_with_diagram, create_meme")
                print("Running on http://127.0.0.1:8007")
                
                config = uvicorn.Config(app, host="127.0.0.1", port=8007, log_level="info")
                server = uvicorn.Server(config)
                await server.serve()
        
        asyncio.run(run_server())
    else:
        # Default FastMCP stdio mode
        mcp.run()