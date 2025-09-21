#!/usr/bin/env python3
"""
Scrimba-style Teaching MCP Server
Step-by-step interactive learning
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("scrimba-tools")

# Simple lesson storage
CURRENT_LESSON = {
    "topic": None,
    "step": 0,
    "total_steps": 0
}

LESSONS = {
    "variables": {
        "title": "Understanding Variables",
        "steps": [
            {
                "explanation": "Variables are containers for storing data. Think of them as labeled boxes.",
                "code": "name = 'Alice'\nage = 25",
                "output": "# name now contains 'Alice'\n# age now contains 25"
            },
            {
                "explanation": "You can change what's inside a variable anytime.",
                "code": "age = 26  # Birthday!\nprint(f'{name} is now {age}')",
                "output": "Alice is now 26"
            },
            {
                "explanation": "Variables can hold different types: numbers, text, lists, etc.",
                "code": "count = 42          # integer\nprice = 19.99       # float\nis_ready = True     # boolean",
                "output": "# Three different data types stored"
            }
        ]
    },
    "loops": {
        "title": "Mastering Loops",
        "steps": [
            {
                "explanation": "Loops repeat code. A 'for' loop runs a specific number of times.",
                "code": "for i in range(3):\n    print(f'Count: {i}')",
                "output": "Count: 0\nCount: 1\nCount: 2"
            },
            {
                "explanation": "While loops continue until a condition becomes false.",
                "code": "counter = 0\nwhile counter < 3:\n    print(f'Counter: {counter}')\n    counter += 1",
                "output": "Counter: 0\nCounter: 1\nCounter: 2"
            }
        ]
    }
}

@mcp.tool()
async def show_lesson(
    topic: str,
    step: Optional[int] = 1
) -> str:
    """
    Display a specific lesson step with code and explanation.
    
    Args:
        topic: Lesson topic (e.g., "variables", "loops")
        step: Step number (default: 1)
    
    Returns:
        Formatted lesson content
    """
    if topic not in LESSONS:
        return f"❌ Unknown topic: {topic}\nAvailable: {', '.join(LESSONS.keys())}"
    
    lesson = LESSONS[topic]
    max_steps = len(lesson["steps"])
    
    if step < 1 or step > max_steps:
        return f"❌ Invalid step. {topic} has {max_steps} steps."
    
    # Update current lesson tracking
    CURRENT_LESSON["topic"] = topic
    CURRENT_LESSON["step"] = step
    CURRENT_LESSON["total_steps"] = max_steps
    
    step_data = lesson["steps"][step - 1]
    
    result = f"""Hey buddy! This is going to be SO much fun! 🎉

📚 **{lesson['title']}** - Step {step}/{max_steps}
{'='*40}

**Let me show you something cool:**
{step_data['explanation']}

**Type this out - don't copy paste!**
```python
{step_data['code']}
```

**When you run it, you'll see:**
```
{step_data['output']}
```

🎯 **YOUR TURN!** Go ahead and try this RIGHT NOW!
Pause here and code it yourself!

When done, type 'next' for more excitement!"""
    
    return result

@mcp.tool()
async def next() -> str:
    """
    Move to the next step in the current lesson.
    
    Returns:
        Next lesson step or completion message
    """
    if not CURRENT_LESSON["topic"]:
        return """Hey buddy! Looks like we haven't started a lesson yet! 
        
Let's fix that RIGHT NOW! Try:
- "teach me variables" to learn about storing data
- "teach me loops" to learn about repeating code

The journey of a thousand apps starts with a single lesson! 🚀"""
    
    topic = CURRENT_LESSON["topic"]
    current_step = CURRENT_LESSON["step"]
    total_steps = CURRENT_LESSON["total_steps"]
    
    if current_step >= total_steps:
        return f"""🎉 **BOOM! You CRUSHED the '{topic}' lesson!** 

You just went from zero to DANGEROUS with this concept! 
This is HUGE - you're officially thinking like a programmer now!

Ready to solidify those skills? Let's put them to work!
Type 'give_challenge' and let's see what you can build! 

Remember: The only way to learn to code is to write a lot of code! 💪"""
    
    return await show_lesson(topic, current_step + 1)

@mcp.tool()
async def previous() -> str:
    """
    Go back to the previous step.
    
    Returns:
        Previous lesson step
    """
    if not CURRENT_LESSON["topic"]:
        return """Hey buddy! No lesson is running right now!

Want to start learning? Try:
- "teach me variables" - the foundation of everything!
- "teach me loops" - make your code work smarter!

Let's get this party started! 🎉"""
    
    topic = CURRENT_LESSON["topic"]
    current_step = CURRENT_LESSON["step"]
    
    if current_step <= 1:
        return """Whoa there! You're already at the beginning! 🏁

This is step 1 - the starting line!
Review it as many times as you want - repetition is KEY!

When ready, type 'next' to continue forward!"""
    
    return await show_lesson(topic, current_step - 1)

@mcp.tool()
async def give_challenge(
    difficulty: Optional[str] = "easy"
) -> str:
    """
    Give a coding challenge to practice immediately.
    
    Args:
        difficulty: "easy" (1 min), "medium" (2 min), or "hard" (3 min)
    
    Returns:
        Challenge instructions with specific tasks
    """
    challenges = {
        "easy": [
            {
                "task": "Create two variables:\n- firstName with your first name\n- lastName with your last name",
                "time": "1 minute",
                "hint": "let firstName = 'Your Name'"
            },
            {
                "task": "Create a variable called age and set it to your age.\nThen create doubleAge that's twice your age.",
                "time": "1 minute", 
                "hint": "let age = 25; let doubleAge = age * 2"
            }
        ],
        "medium": [
            {
                "task": "Write a function called greet that:\n1. Takes a name parameter\n2. Returns 'Hello ' + name\n3. Test it with console.log",
                "time": "2 minutes",
                "hint": "function greet(name) { return ... }"
            },
            {
                "task": "Create an array of 3 favorite foods.\nThen add a 4th item using push().",
                "time": "2 minutes",
                "hint": "let foods = ['pizza', ...]; foods.push('...')"
            }
        ],
        "hard": [
            {
                "task": "Build a counter:\n1. Variable count starting at 0\n2. Function increment() that adds 1\n3. Function save() that stores count in an array\n4. Test all functions",
                "time": "3 minutes",
                "hint": "let count = 0; let saves = []; function increment() { count += 1 }"
            }
        ]
    }
    
    level_challenges = challenges.get(difficulty, challenges["easy"])
    import random
    challenge = random.choice(level_challenges)
    
    return f"""Hey buddy! Time to write some code! This is where it gets FUN! 🚀

🎯 **CHALLENGE TIME!** ({difficulty.upper()})

**Your mission ({challenge['time']}):**
{challenge['task']}

**Go ahead and do this RIGHT NOW!**
Don't overthink it - just start typing!

The first time feels weird, but it becomes second nature!

When you're done (or stuck), show me your code!
Remember: Making mistakes is how we learn! That's totally okay!"""

@mcp.tool()
async def check_code(
    code: str
) -> str:
    """
    Check user's code solution with encouraging Scrimba-style feedback.
    
    Args:
        code: The user's code solution
    
    Returns:
        Encouraging feedback with specific praise
    """
    # Basic checks for common patterns
    feedback = []
    
    # Check for variables
    if "let " in code or "const " in code or "var " in code:
        feedback.append("✓ Great job creating variables!")
    
    # Check for functions
    if "function" in code or "=>" in code:
        feedback.append("✓ Awesome function work!")
    
    # Check for console.log
    if "console.log" in code:
        feedback.append("✓ YES! Console.log is your best friend!")
    
    # Check for arrays
    if "[" in code and "]" in code:
        feedback.append("✓ Nice array skills!")
    
    # Check for common mistakes
    warnings = []
    if "=" in code and not "==" in code and not "let" in code and not "const" in code:
        warnings.append("💡 Oops! Super common mistake - did you forget 'let' or 'const'?")
    
    if "functoin" in code:
        warnings.append("💡 Tiny typo: 'functoin' should be 'function' - happens to everyone!")
    
    # Build response with Per Borgen energy
    if warnings:
        response = "Oops! Super common mistake! I made this EXACT error when I started! 😄\n\n"
        response += "\n".join(warnings) + "\n\n"
        response += "JavaScript is telling us what's wrong - that's actually helpful!\n"
        response += "Try again with those fixes - you've got this!\n\n"
    else:
        response = "🎉 **GREAT JOB!** You just wrote REAL CODE! This is HUGE!\n\n"
        
        if feedback:
            response += "Look what you did:\n"
            response += "\n".join(feedback) + "\n\n"
        
        response += "Your skills are becoming DANGEROUS! 🔥\n\n"
        response += "The only way to learn to code is to write a lot of code - and you're doing it!\n\n"
        response += "Want another challenge? I've got TONS! Just say the word!"
    
    return response

@mcp.tool()
async def celebrate(
    achievement: Optional[str] = "progress"
) -> str:
    """
    Celebrate user's achievement with Scrimba-style enthusiasm.
    
    Args:
        achievement: What to celebrate (e.g., "first_variable", "completed_lesson", "fixed_bug")
    
    Returns:
        Enthusiastic celebration message
    """
    celebrations = {
        "first_variable": """🎉 **THIS IS HUGE!** You just created your FIRST variable!
        
You're officially NOT like everyone else - you're a PROGRAMMER now!
Most people NEVER get this far! But YOU did!

I still remember my first variable - it felt like MAGIC! ✨""",
        
        "first_function": """🚀 **MIND = BLOWN!** You just wrote a FUNCTION!
        
This is MASSIVE! You can now create reusable code blocks!
Functions are the building blocks of EVERY app you've ever used!

You're thinking like a developer now! SO exciting!""",
        
        "completed_lesson": """💪 **BOOM! LESSON CRUSHED!**
        
Give yourself a MASSIVE pat on the back!
You just learned something 99% of people never will!

Your brain is literally rewiring itself right now! 🧠""",
        
        "fixed_bug": """🔧 **YES YES YES!** You just DEBUGGED code!
        
This is what REAL developers do ALL DAY!
You didn't give up - you SOLVED it!

Bugs are not failures - they're TEACHERS! And you're learning FAST!""",
        
        "progress": """🌟 **Your skills are becoming DANGEROUS!**
        
You're making progress that would make professional developers proud!
Keep this momentum going!""",
        
        "project": """🏆 **OH MY GOODNESS!** You built something REAL!
        
This isn't just practice - this SOLVES actual problems!
You could show this to people and they'd be IMPRESSED!

You're not just learning - you're CREATING! That's the difference!"""
    }
    
    message = celebrations.get(achievement, celebrations["progress"])
    
    return f"""{message}

Remember: The only way to learn to code is to write a LOT of code!
And buddy... you're doing EXACTLY that! 

This is SO exciting! Let's keep the momentum going! 🚀💪"""

# Progress tracking
USER_PROGRESS = {
    "concepts_learned": [],
    "challenges_completed": 0,
    "current_level": "beginner"
}

@mcp.tool()
async def show_hint(
    level: Optional[int] = 1
) -> str:
    """
    Give progressive hints without revealing the full answer.
    
    Args:
        level: Hint level (1=subtle, 2=clearer, 3=almost there)
    
    Returns:
        Progressive hint based on level
    """
    if not CURRENT_LESSON["topic"]:
        # Give generic hints for challenges
        hints = {
            1: "💡 **Tiny nudge:** Variables are containers... think about HOW we create them in JavaScript!",
            2: "💡 **Getting warmer!** Remember: 'let' is your friend! Pattern: let [something] = [value]",
            3: "💡 **SO CLOSE!** Try this exact pattern: let count = 0 (but with your own variable name!)"
        }
    else:
        # Context-aware hints based on current lesson
        topic = CURRENT_LESSON["topic"]
        if topic == "variables":
            hints = {
                1: "💡 **Think about it:** Variables are like labeled boxes that hold stuff. How do we CREATE a box?",
                2: "💡 **Here's the secret:** Use 'let' to create a new variable box! let [name] = [stuff]",
                3: "💡 **You're RIGHT THERE!** Pattern: let name = 'Per' or let age = 25"
            }
        elif topic == "loops":
            hints = {
                1: "💡 **Loops are POWERFUL!** They let you repeat code without typing it 100 times!",
                2: "💡 **The magic formula:** for(let i = 0; i < max; i++) - this runs 'max' times!",
                3: "💡 **Copy this and modify:** for(let i = 0; i < 3; i++) { console.log('Hello!') }"
            }
        else:
            hints = {
                1: "💡 **Step back for a second:** What are you trying to accomplish? Break it into baby steps!",
                2: "💡 **Make it SIMPLER:** Start with the most basic version, then add complexity",
                3: "💡 **Just START typing:** Even if it's wrong, we can fix it! That's how we learn!"
            }
    
    hint = hints.get(level, hints[1])
    
    prefix = [
        "Hey buddy! Stuck? That's TOTALLY normal! Let me help... 🤔",
        "Alright, let me give you a BIGGER hint! This is exciting! 🎯",
        "OK buddy, I'm basically giving you the answer here! You've GOT this! 🚀"
    ]
    
    return f"""{prefix[level-1] if level <= 3 else "Hey buddy! Let me help!"}

{hint}

{"Want more help? Type 'show_hint' with level 2 or 3!" if level < 3 else "Now GO! Type it out! Making mistakes is how we learn!"}

Remember: I got stuck here too when I started. EVERYONE does! That's the journey! 💪"""

@mcp.tool()
async def track_progress() -> str:
    """
    Show user's learning progress with checkmarks.
    
    Returns:
        Progress summary with achievements
    """
    # Update progress based on activities
    if CURRENT_LESSON["topic"] and CURRENT_LESSON["topic"] not in USER_PROGRESS["concepts_learned"]:
        USER_PROGRESS["concepts_learned"].append(CURRENT_LESSON["topic"])
    
    # Build progress report
    report = """Hey buddy! Let's see how DANGEROUS you've become! 🔥

📊 **YOUR EPIC CODING JOURNEY**
""" + "=" * 40 + """

**🎯 Concepts You've CONQUERED:**
"""
    
    concepts = {
        "variables": "✅ Variables - You can store ANY data now!",
        "loops": "✅ Loops - You make computers do the repetitive work!",
        "functions": "✅ Functions - You write code ONCE, use it EVERYWHERE!",
        "arrays": "✅ Arrays - You handle lists like a PRO!",
        "objects": "✅ Objects - You structure complex data!"
    }
    
    if USER_PROGRESS["concepts_learned"]:
        for concept in USER_PROGRESS["concepts_learned"]:
            if concept in concepts:
                report += f"{concepts[concept]}\n"
        report += "\n**THIS IS HUGE!** Each concept makes you exponentially more powerful!\n"
    else:
        report += "Ready to start? Your first lesson will BLOW YOUR MIND! 🚀\n"
    
    report += f"\n**⚡ Challenges CRUSHED:** {USER_PROGRESS['challenges_completed']}"
    
    if USER_PROGRESS["challenges_completed"] > 0:
        report += f" (That's {USER_PROGRESS['challenges_completed']} real problems SOLVED!)\n"
    else:
        report += " (Your first challenge awaits!)\n"
    
    report += f"**🏆 Current Level:** {USER_PROGRESS['current_level'].upper()}\n\n"
    
    # Motivational message based on progress
    if USER_PROGRESS["challenges_completed"] >= 10:
        report += """🔥🔥🔥 **UNSTOPPABLE!** 🔥🔥🔥
You've written more code than 99% of people EVER will!
Your skills are becoming SERIOUSLY dangerous!

At this rate, you'll be building REAL apps in no time!"""
    elif USER_PROGRESS["challenges_completed"] > 5:
        report += """🔥 **You're on FIRE!**
Look at you go! This momentum is EVERYTHING!
Professional developers started EXACTLY where you are now!"""
    elif USER_PROGRESS["challenges_completed"] > 2:
        report += """💪 **You're gaining SERIOUS momentum!**
Those first challenges were the HARDEST - and you crushed them!
It only gets more fun from here!"""
    elif USER_PROGRESS["challenges_completed"] > 0:
        report += """🌟 **You've STARTED! That's the hardest part!**
Most people never write their first line of code - but YOU DID!
Keep going - this is where it gets exciting!"""
    else:
        report += """🚀 **Your journey is about to begin!**
The first step is the most important one!
Let's write some code and change your life!"""
    
    report += """\n\nRemember: The only way to learn to code is to write a LOT of code!
And buddy... you're doing EXACTLY that! Let's keep going! 💪"""
    
    return report

@mcp.tool()
async def start_project(
    project_name: Optional[str] = "passenger_counter"
) -> str:
    """
    Start a real project with step-by-step guidance.
    
    Args:
        project_name: "passenger_counter", "blackjack", or "chrome_extension"
    
    Returns:
        Project setup and first steps
    """
    projects = {
        "passenger_counter": {
            "story": "When I was 19, I had to count people entering the subway. SO boring! My finger hurt from clicking the mechanical counter!",
            "goal": "Build an app to count passengers (and save fingers!)",
            "why": "This was my ACTUAL problem! And coding solved it!",
            "steps": [
                "1. Create variable: let count = 0 (your counter starts at zero)",
                "2. Create function: increment() to add 1 each time",  
                "3. Add button in HTML (what users will click)",
                "4. Connect button to function (make it WORK!)",
                "5. Display count on page (show the number!)"
            ],
            "starter": """let count = 0  // This is your counter!

function increment() {
    // TODO: Add 1 to count
    // TODO: Update what's shown on screen
}

// Your turn! Make this function actually COUNT!"""
        },
        "blackjack": {
            "story": "I won 100 euros playing Blackjack in Prague! Then lost it all... but I learned probability!",
            "goal": "Build a REAL Blackjack game",
            "why": "Games teach logic, conditions, and state management!",
            "steps": [
                "1. Create variables for your cards",
                "2. Make a sum calculation function",
                "3. Check if you hit Blackjack (21!)",
                "4. Create 'draw new card' function",
                "5. Determine who wins!"
            ],
            "starter": """let firstCard = 11   // Ace or Jack/Queen/King!
let secondCard = 10  // Face card!
let sum = firstCard + secondCard  // What's your total?

// TODO: Create a function to check if you have Blackjack!
// Hint: Blackjack means sum equals... what?"""
        },
        "chrome_extension": {
            "story": "I got tired of manually checking things on websites. So I automated it!",
            "goal": "Build a Chrome Extension that actually WORKS",
            "why": "Extensions can save you HOURS of repetitive work!",
            "steps": [
                "1. Create manifest.json (extension config)",
                "2. Build popup HTML interface",
                "3. Add JavaScript functionality",
                "4. Connect to Chrome APIs",
                "5. Test in real browser!"
            ],
            "starter": """// manifest.json tells Chrome about your extension
{
    "name": "My First Extension",
    "version": "1.0",
    "manifest_version": 3
    // TODO: Add more configuration
}"""
        }
    }
    
    project = projects.get(project_name, projects["passenger_counter"])
    
    return f"""Hey buddy! This is SO EXCITING! We're building something REAL! 🚀

🎯 **PROJECT: {project_name.upper().replace('_', ' ')}**

**MY STORY:** {project['story']}

**WHY THIS MATTERS:** {project['why']}

**WHAT WE'RE BUILDING:** {project['goal']}

**🔨 BUILD STEPS (We'll do these together!):**
{chr(10).join(project['steps'])}

**📝 STARTER CODE (Type this out - don't copy!):**
```javascript
{project['starter']}
```

⚡ **YOUR MISSION RIGHT NOW:**
Complete Step 1! Just START! Don't overthink it!

**Pro tip:** The first line of code is the hardest. After that, momentum takes over!

Type your code and show me! If you get stuck, ask for a hint!

**This is not just practice - this solves REAL problems!**
Let's GO buddy! Your first real project starts NOW! 🔥"""

@mcp.tool()
async def console_log_check(
    code: str
) -> str:
    """
    Console.log Driven Development - verify EVERYTHING with console.log
    Following exact Scrimba examples
    """
    has_console = "console.log" in code
    
    if not has_console:
        # Count variables/functions that need verification
        needs_verification = []
        if "let " in code or "const " in code:
            needs_verification.append("variables")
        if "function" in code:
            needs_verification.append("functions")
        if "=" in code:
            needs_verification.append("assignments")
            
        return f"""Hey buddy! WAIT! Let's verify your code works! 

**Console.log Driven Development** - The Scrimba Way:

Step 1: You wrote code ✅
Step 2: NOW VERIFY IT! Add console.log() 🔍
Step 3: See the magic happen! 

{f"I see you have {', '.join(needs_verification)} - let's CHECK them!" if needs_verification else ""}

Add this after EVERY variable:
```javascript
let myAge = 25
console.log(myAge)  // SEE it work!
```

This is how REAL developers code - verify EVERYTHING!
Try again with console.log!"""
    
    # They have console.log - celebrate!
    return f"""🎉 **PERFECT!** You're doing Console.log Driven Development!

You wrote → You verified → You SAW it work!

This is EXACTLY how I code:
1. Write one line
2. Console.log it
3. Celebrate when it works!

Your code is ALIVE and you can SEE it! 
This is how you'll catch bugs INSTANTLY!

Keep going - console.log EVERYTHING! It's your superpower! 💪"""

@mcp.tool()
async def learn_by_breaking(
    concept: str
) -> str:
    """
    Error-First Learning - intentionally break things to learn debugging
    
    Args:
        concept: The concept to teach through errors
    
    Returns:
        Broken code examples with guided fixes
    """
    error_examples = {
        "variables": {
            "title": "Let's BREAK variables on purpose!",
            "examples": [
                {
                    "broken": "console.log(myName)\nlet myName = 'Per'",
                    "error": "ReferenceError: myName is not defined",
                    "explanation": "JavaScript reads TOP to BOTTOM! It doesn't know about myName yet!",
                    "fix": "let myName = 'Per'\nconsole.log(myName)",
                    "lesson": "ALWAYS declare before using!"
                },
                {
                    "broken": "let my-name = 'Per'",
                    "error": "SyntaxError: Unexpected token '-'",
                    "explanation": "No hyphens in variable names! JavaScript thinks you're subtracting!",
                    "fix": "let myName = 'Per'  // or my_name",
                    "lesson": "Use camelCase or underscores!"
                },
                {
                    "broken": "let name = Per",
                    "error": "ReferenceError: Per is not defined",
                    "explanation": "JavaScript thinks Per is a variable! Text needs quotes!",
                    "fix": "let name = 'Per'",
                    "lesson": "Strings ALWAYS need quotes!"
                }
            ]
        },
        "functions": {
            "title": "Let's BREAK functions and FIX them!",
            "examples": [
                {
                    "broken": "greet('Per')\nfunction greet(name) { return 'Hello ' + name }",
                    "error": "ReferenceError: greet is not defined",
                    "explanation": "You can't use a function before it exists!",
                    "fix": "function greet(name) { return 'Hello ' + name }\ngreet('Per')",
                    "lesson": "Define functions FIRST!"
                },
                {
                    "broken": "function greet name { }",
                    "error": "SyntaxError: Unexpected identifier",
                    "explanation": "Functions need parentheses for parameters!",
                    "fix": "function greet(name) { }",
                    "lesson": "Always use () even if empty!"
                }
            ]
        }
    }
    
    if concept not in error_examples:
        concept = "variables"  # Default
    
    examples = error_examples[concept]
    result = f"""🔥 **ERROR-FIRST LEARNING** - {examples['title']}

I'm going to show you BROKEN code on purpose!
Why? Because debugging is a SUPERPOWER! 

"""
    
    for i, ex in enumerate(examples['examples'], 1):
        result += f"""
**Break #{i}:**
```javascript
{ex['broken']}
```

💥 **Error:** `{ex['error']}`

**What happened?** {ex['explanation']}

**THE FIX:**
```javascript
{ex['fix']}
```

**LESSON:** {ex['lesson']}

---"""
    
    result += """

Remember: EVERY developer makes these mistakes!
The difference? Now you know how to FIX them!

Debugging isn't failure - it's LEARNING! 🚀"""
    
    return result

@mcp.tool()
async def progressive_challenge(
    level: int = 1
) -> str:
    """
    Progressive complexity - exactly 5 levels for every concept
    
    Args:
        level: Current level (1-5)
    
    Returns:
        Challenge for that exact level with CDD built in
    """
    levels = {
        1: {
            "title": "Level 1: Basic Declaration",
            "time": "60 seconds",
            "challenge": "let count = 0",
            "verify": "console.log(count)",
            "expected": "0",
            "next": "We're starting simple - just storing data!"
        },
        2: {
            "title": "Level 2: Reassignment", 
            "time": "90 seconds",
            "challenge": "count = count + 1",
            "verify": "console.log(count)",
            "expected": "1",
            "next": "Now we're CHANGING data!"
        },
        3: {
            "title": "Level 3: Shorthand",
            "time": "60 seconds",
            "challenge": "count += 1",
            "verify": "console.log(count)",
            "expected": "2",
            "next": "Same thing, less typing!"
        },
        4: {
            "title": "Level 4: Pro Syntax",
            "time": "60 seconds",
            "challenge": "count++",
            "verify": "console.log(count)",
            "expected": "3",
            "next": "The PRO way to add 1!"
        },
        5: {
            "title": "Level 5: BUILD THE APP!",
            "time": "180 seconds",
            "challenge": "Build the passenger counter!",
            "project": """
let count = 0

function increment() {
    count++
    console.log(count)
}

// Test it!
increment()  // 1
increment()  // 2
increment()  // 3""",
            "next": "YOU'RE BUILDING REAL APPS!"
        }
    }
    
    current = levels[level]
    
    if level < 5:
        return f"""⚡ **PROGRESSIVE CHALLENGE** - {current['title']}

⏱️ Time: {current['time']}

**Your mission:**
```javascript
{current['challenge']}
{current['verify']}  // ALWAYS verify!
```

**Expected output:** `{current['expected']}`

{current['next']}

Type it out RIGHT NOW! Don't copy-paste!
When done, show me your console output!"""
    
    else:  # Level 5 - Project time!
        return f"""🚀 **{current['title']}**

⏱️ Time: {current['time']}

**Build this COMPLETE app:**
```javascript
{current['project']}
```

This is it! A REAL working counter!
Just like I needed at the subway station!

{current['next']}

GO GO GO! Show me when it's working!"""

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
                print("Scrimba Teaching MCP Server")
                print("============================")
                print("Tools: show_lesson, next, previous")
                
                config = uvicorn.Config(app, host="127.0.0.1", port=8006, log_level="info")
                server = uvicorn.Server(config)
                await server.serve()
        
        asyncio.run(run_server())
    else:
        mcp.run()