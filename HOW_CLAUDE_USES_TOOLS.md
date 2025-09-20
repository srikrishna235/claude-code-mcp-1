# How Claude Code Automatically Uses MCP Tools

## The Magic: Tool Selection is Automatic!

When you run:
```bash
claude "What's the weather in Paris?"
```

Here's what happens behind the scenes:

### 1. Claude Receives Query
Claude Code gets your question: "What's the weather in Paris?"

### 2. Claude Sees Available Tools
From connected MCP servers, Claude knows it has:
- `get_temperature` - Get current temperature for a city
- `get_weather_forecast` - Get weather forecast
- `compare_weather` - Compare weather between cities
- Plus all built-in tools (Read, Write, Bash, etc.)

### 3. Claude Decides Which Tool
Claude's AI model analyzes:
- User asks about "weather" → weather-related tool needed
- Mentions "Paris" → city parameter
- Present tense "what's" → current weather, not forecast
- **Decision: Use `get_temperature` with city="Paris"**

### 4. Claude Calls the Tool
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_temperature",
    "arguments": {"city": "Paris"}
  }
}
```

### 5. MCP Server Responds
Weather server fetches data and returns:
```
Weather in Paris:
🌡️ Temperature: 21°C
☁️ Conditions: Patchy rain nearby
💧 Humidity: 64%
```

### 6. Claude Formats Response
Claude takes the tool result and presents it conversationally:
"The current weather in Paris is 21°C with patchy rain nearby. The humidity is 64%. You might want to bring an umbrella!"

## Examples of Automatic Tool Selection

### Query → Tool Mapping

| User Query | Claude Selects | Why |
|------------|---------------|-----|
| "Weather in London?" | `get_temperature("London")` | Current weather query |
| "Will it rain in Tokyo tomorrow?" | `get_weather_forecast("Tokyo", 1)` | Future tense = forecast |
| "Compare NYC vs LA weather" | `compare_weather("NYC,LA")` | "Compare" keyword |
| "What should I wear in Berlin?" | `get_temperature("Berlin")` | Needs current conditions |
| "Planning trip to Rome next week" | `get_weather_forecast("Rome", 3)` | Future planning |

## No Special Syntax Needed!

You DON'T need to:
- Specify which tool to use
- Format parameters specially  
- Use special commands
- Create agents or scripts

Just ask naturally, and Claude figures it out!

## Under the Hood: Claude's Decision Process

```python
# Pseudo-code of Claude's internal logic
def process_query(user_input):
    # 1. Parse intent
    intent = analyze_intent(user_input)  # "get_weather"
    
    # 2. Extract entities  
    entities = extract_entities(user_input)  # {"city": "Paris"}
    
    # 3. Match to available tools
    available_tools = get_mcp_tools() + get_builtin_tools()
    
    # 4. Score each tool for relevance
    for tool in available_tools:
        score = calculate_relevance(tool, intent, entities)
    
    # 5. Pick best tool
    best_tool = max(available_tools, key=score)
    
    # 6. Call it
    result = call_tool(best_tool, entities)
    
    # 7. Generate response
    return generate_natural_response(result)
```

## Testing It Yourself

With weather server running on port 8003:

```bash
# Connect it (only need to do once)
claude mcp add weather http://localhost:8003

# Now just use Claude normally!
claude "Is it sunny in Sydney?"
claude "Weekend weather for Chicago?"  
claude "Warmest city: Miami, Phoenix, or Vegas?"
```

Claude automatically picks the right weather tool every time!

## The Beauty of MCP

This is why MCP (Model Context Protocol) is powerful:
1. **Tool providers** just define functions
2. **Claude** automatically knows when to use them
3. **Users** just ask questions naturally

No glue code, no routing logic, no manual tool selection needed!