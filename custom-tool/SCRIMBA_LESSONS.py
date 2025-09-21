"""
Scrimba-style Micro-Lessons Following Exact Methodology
"""

MICRO_LESSONS = {
    "variables": {
        "hook": "When I was 19, I had to count subway passengers in the cold. My fingers would freeze and I'd lose count after 50... If only I had a variable to store the count!",
        "levels": [
            {
                "time": "60s",
                "concept": "let count = 0",
                "explanation": "Read this as 'let count be zero' - super natural!",
                "challenge": "Create a variable called myAge with your age. GO!",
                "verification": "console.log(myAge)  // See it work!",
                "celebration": "🎉 HUGE! You just stored your FIRST piece of data!"
            },
            {
                "time": "90s", 
                "concept": "count = count + 1",
                "explanation": "This adds 1 to count - like clicking a counter!",
                "challenge": "Add 1 to your myAge variable. Type it out!",
                "verification": "console.log(myAge)  // Should be 1 more!",
                "celebration": "💪 You just CHANGED data! Your code is alive!"
            },
            {
                "time": "60s",
                "concept": "count += 1",
                "explanation": "Shorthand - same thing, less typing!",
                "challenge": "Use += to add 5 to myAge",
                "verification": "console.log(myAge)  // Jumped by 5!",
                "celebration": "🚀 You're writing like a PRO already!"
            },
            {
                "time": "60s",
                "concept": "count++",
                "explanation": "The FASTEST way to add 1!",
                "challenge": "Create a score variable at 0, then score++ three times",
                "verification": "console.log(score)  // Should be 3!",
                "celebration": "🔥 You've mastered ALL increment methods!"
            },
            {
                "time": "180s",
                "concept": "Build Passenger Counter!",
                "explanation": "Let's solve my subway problem!",
                "challenge": "Create: count=0, function increment(){count++}, test it!",
                "verification": "increment(); increment(); console.log(count) // 2!",
                "celebration": "🎊 YOU BUILT A REAL APP! This could save someone's fingers!"
            }
        ]
    },
    "functions": {
        "hook": "I used to copy-paste the SAME code 50 times. Then Per showed me functions - it was like discovering CTRL+C!",
        "levels": [
            {
                "time": "60s",
                "concept": "function greet() { console.log('Hi!') }",
                "explanation": "Functions are reusable code blocks!",
                "challenge": "Create function sayHello() that logs 'Hello!'",
                "verification": "sayHello()  // Call it!",
                "celebration": "⚡ Your FIRST function! You can now reuse code!"
            },
            {
                "time": "90s",
                "concept": "function greet(name) { ... }",
                "explanation": "Parameters make functions flexible!",
                "challenge": "Make greet(name) return 'Hello ' + name",
                "verification": "console.log(greet('Per'))  // 'Hello Per'",
                "celebration": "🎯 Functions with parameters! SO powerful!"
            },
            {
                "time": "90s",
                "concept": "return values",
                "explanation": "Functions can give back results!",
                "challenge": "Create add(a, b) that RETURNS a + b",
                "verification": "console.log(add(5, 3))  // 8",
                "celebration": "🏆 You're combining and returning! DANGEROUS skills!"
            },
            {
                "time": "120s",
                "concept": "Multiple functions working together",
                "explanation": "Functions can call other functions!",
                "challenge": "Create double(n) and triple(n), then use both!",
                "verification": "console.log(triple(double(5)))  // 30",
                "celebration": "🎪 Function CIRCUS! They're working together!"
            },
            {
                "time": "180s",
                "concept": "Build Calculator!",
                "explanation": "Real calculator with add, subtract, multiply!",
                "challenge": "Create 3 functions, test each!",
                "verification": "console.log(multiply(add(2,3), 4))  // 20",
                "celebration": "🌟 YOU BUILT A CALCULATOR! Mom would be proud!"
            }
        ]
    }
}

# Project-Based Learning Path
PROJECTS = {
    "passenger_counter": {
        "story": "My fingers literally hurt from clicking mechanical counters in the cold!",
        "duration": "30 min",
        "concepts": ["variables", "functions", "DOM"],
        "milestones": [
            {"task": "let count = 0", "celebrate": "Counter initialized!"},
            {"task": "function increment()", "celebrate": "Increment working!"},
            {"task": "Display in HTML", "celebrate": "It's VISIBLE!"},
            {"task": "Save function", "celebrate": "Data persists!"},
            {"task": "Reset function", "celebrate": "COMPLETE APP!"}
        ]
    },
    "blackjack": {
        "story": "I won 100 euros in Prague... then lost it all. Let's build the game!",
        "duration": "45 min",
        "concepts": ["conditionals", "arrays", "logic"],
        "milestones": [
            {"task": "Deal 2 cards", "celebrate": "Cards dealt!"},
            {"task": "Calculate sum", "celebrate": "Math working!"},
            {"task": "Check for 21", "celebrate": "Blackjack detection!"},
            {"task": "Draw new card", "celebrate": "Game logic complete!"},
            {"task": "Determine winner", "celebrate": "CASINO READY!"}
        ]
    }
}

# Celebration Messages (Progressive Intensity)
CELEBRATIONS = {
    "first_time": [
        "🎉 HUGE! Your FIRST {}!",
        "🚀 You just learned {}! This is MASSIVE!",
        "💪 {} mastered! Give yourself a pat on the back!"
    ],
    "milestone": [
        "🔥 You're on FIRE! {} in a row!",
        "⚡ UNSTOPPABLE! {} challenges crushed!",
        "👑 LEGENDARY! You've conquered {}!"
    ],
    "project": [
        "🏆 YOU BUILT SOMETHING REAL!",
        "🎊 This isn't practice - this SOLVES problems!",
        "🌟 You could SHIP this! People would USE it!"
    ]
}

# Error Encouragement
ERRORS = {
    "syntax": "Oops! Super common! I make this mistake daily!",
    "undefined": "JavaScript is confused - let's help it!",
    "logic": "The computer did EXACTLY what you said - let's refine!",
    "typo": "Typo! My nemesis! One letter off!"
}

# Timing Structure
TIMING = {
    "hook": 20,          # Personal story
    "concept": 60,       # One thing only  
    "challenge": 120,    # Immediate practice
    "celebrate": 10,     # Quick win
    "total": 210        # 3.5 minutes max
}