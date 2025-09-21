#!/usr/bin/env python3
"""
Scrimba Teaching MCP Server
Interactive programming teacher using Scrimba methodology
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
import json

mcp = FastMCP("scrimba-teaching")

# Session state
SESSION_STATE = {
    "current_lesson": None,
    "current_step": 1,
    "challenges_completed": 0,
    "concepts_learned": [],
    "user_code_history": []
}

# Scrimba methodology constants
MICRO_LESSON_STRUCTURE = {
    "hook_duration": 20,
    "concept_duration": 60,
    "challenge_duration": 120,
    "celebration_duration": 10
}

COMPLEXITY_LEVELS = [
    "Basic declaration",
    "Modification/reassignment", 
    "Shorthand syntax",
    "Advanced usage",
    "BUILD REAL APP!"
]

# Lesson content
LESSONS = {
    "variables": {
        "hook": "When I was 19, I had to count subway passengers in the cold...",
        "title": "Variables - Your First Storage Box!",
        "levels": [
            {
                "concept": "let count = 0",
                "explanation": "Read this as 'let count be zero' - super natural!",
                "challenge": "Create a variable called myAge with your age. GO!",
                "console_log": "console.log(myAge)",
                "celebration": "🎉 HUGE! You just stored your FIRST piece of data!"
            }
        ]
    },
    "functions": {
        "hook": "I used to copy-paste the SAME code 50 times...",
        "title": "Functions - Reusable Magic!",
        "levels": [
            {
                "concept": "function greet() { console.log('Hi!') }",
                "explanation": "Functions are reusable code blocks!",
                "challenge": "Create function sayHello() that logs 'Hello!'",
                "console_log": "sayHello()",
                "celebration": "⚡ Your FIRST function!"
            }
        ]
    },
    "loops": {
        "hook": "I once had to create 100 user profiles manually...",
        "title": "Loops - Automation Magic!",
        "levels": [
            {
                "concept": "for(let i = 0; i < 5; i++)",
                "explanation": "The classic for loop - repeat 5 times!",
                "challenge": "Count from 0 to 4 with a for loop",
                "console_log": "// Should print 0, 1, 2, 3, 4",
                "celebration": "🔄 Your first loop!"
            }
        ]
    }
}

CHALLENGES = {
    "easy": [
        {
            "task": "Create a variable called 'score' and set it to 0",
            "time": "60 seconds",
            "hint": "let score = 0"
        }
    ],
    "medium": [
        {
            "task": "Create a function that adds two numbers",
            "time": "120 seconds",
            "hint": "function add(a, b) { return ... }"
        }
    ],
    "hard": [
        {
            "task": "Create an array and loop through it",
            "time": "180 seconds",
            "hint": "Use .map() or a for loop"
        }
    ]
}

@mcp.tool()
async def teach(topic: str, step: Optional[int] = 1) -> str:
    """Teach a programming concept using Scrimba methodology"""
    
    if topic not in LESSONS:
        return f"Available topics: {', '.join(LESSONS.keys())}"
    
    SESSION_STATE["current_lesson"] = topic
    SESSION_STATE["current_step"] = step
    
    lesson = LESSONS[topic]
    if step > len(lesson["levels"]):
        return "Lesson complete! Start a project to apply what you learned!"
    
    level = lesson["levels"][step - 1]
    
    return f"""📚 **{lesson['title']}** - Level {step}/5

**Hook:** {lesson['hook'] if step == 1 else 'Let\'s go deeper!'}

**Concept:**
```javascript
{level['concept']}
```

**Explanation:** {level['explanation']}

**YOUR CHALLENGE ({MICRO_LESSON_STRUCTURE['challenge_duration']}s):**
{level['challenge']}

**Verify with:**
```javascript
{level['console_log']}
```

{level['celebration']}

Type your solution! Don't think, just DO! 🚀"""

@mcp.tool()
async def give_challenge(difficulty: Optional[str] = "easy") -> str:
    """Give an immediate coding challenge"""
    
    import random
    challenge = random.choice(CHALLENGES.get(difficulty, CHALLENGES["easy"]))
    SESSION_STATE["challenges_completed"] += 1
    
    return f"""⚡ **CHALLENGE TIME!**

**Difficulty:** {difficulty.upper()}
**Time:** {challenge['time']}

📝 **YOUR MISSION:**
{challenge['task']}

💡 **Hint:** {challenge['hint']}

Timer starts... NOW! ⏰"""

@mcp.tool()
async def check_code(code: str) -> str:
    """Check user's code with encouragement"""
    
    SESSION_STATE["user_code_history"].append(code)
    SESSION_STATE["challenges_completed"] += 1
    
    # Simple checks
    has_variable = any(k in code for k in ["let", "const", "var"])
    has_function = "function" in code or "=>" in code
    has_console = "console.log" in code
    
    if has_variable and has_console:
        return "🎉 **PERFECT!** Your code is working! You're becoming DANGEROUS with code! 🔥"
    elif has_variable:
        return "💪 **Great start!** Add console.log() to verify it works!"
    else:
        return "🌟 **Keep going!** Remember: let variableName = value"

@mcp.tool()
async def next() -> str:
    """Progress to next lesson step"""
    
    topic = SESSION_STATE.get("current_lesson", "variables")
    step = SESSION_STATE.get("current_step", 1) + 1
    
    return await teach(topic, step)

@mcp.tool()
async def previous() -> str:
    """Go back to previous step"""
    
    topic = SESSION_STATE.get("current_lesson", "variables")
    step = max(1, SESSION_STATE.get("current_step", 1) - 1)
    
    return await teach(topic, step)

@mcp.tool()
async def show_progress() -> str:
    """Show learning progress"""
    
    challenges = SESSION_STATE["challenges_completed"]
    current = SESSION_STATE.get("current_lesson", "Not started")
    
    level = "BEGINNER 🌱"
    if challenges > 20:
        level = "EXPERT 👑"
    elif challenges > 10:
        level = "INTERMEDIATE ⚡"
    elif challenges > 5:
        level = "ADVANCING 📈"
    
    return f"""📊 **YOUR PROGRESS**

**Current Topic:** {current}
**Challenges Completed:** {challenges}
**Level:** {level}

{'█' * min(challenges, 20)}{'░' * (20 - min(challenges, 20))}
{min(challenges * 5, 100)}% to MASTERY!

Keep coding! You're doing AMAZING! 🚀"""

@mcp.tool()
async def celebrate(achievement: Optional[str] = "progress") -> str:
    """Celebrate user's achievement"""
    
    celebrations = {
        "first_variable": "🎉 YOUR FIRST VARIABLE! This is HUGE!",
        "first_function": "⚡ FIRST FUNCTION! You can now write reusable code!",
        "first_loop": "🔄 LOOP MASTERY! You just automated repetition!",
        "completed_lesson": "🎓 LESSON COMPLETE! You're learning 10x faster!",
        "progress": f"🚀 {SESSION_STATE['challenges_completed']} challenges completed!"
    }
    
    return celebrations.get(achievement, celebrations["progress"])

if __name__ == "__main__":
    mcp.run()