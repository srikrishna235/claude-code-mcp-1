# Agent Implementation Strategy

## The Correct Approach: Let Claude Decide

Based on Claude Code documentation and best practices:

### 1. Natural Tool Usage (Default)
When no `agent_mode` is specified, Claude:
- Sees available MCP tools (weather tools, file tools, etc.)
- Automatically decides when to use them based on the query
- Acts as an expert when appropriate without explicit prompting

### 2. Optional Agent Mode
The `agent_mode` parameter is available but optional:
- `null` (default): Claude works naturally with available tools
- `"general"`: Adds a subtle prompt about available capabilities
- `"weather"`: Explicitly makes Claude a weather expert
- Future: Can add more specialized modes

### 3. How It Works

#### Without Agent Mode:
```
User: "What's the weather in Paris?"
    ↓
Terminal sends: {prompt: "What's the weather in Paris?", agent_mode: null}
    ↓
MCP Wrapper: claude -p "What's the weather in Paris?" --output-format stream-json
    ↓
Claude: Sees weather tools available, naturally uses get_temperature()
    ↓
Response: Weather information
```

#### With Explicit Agent Mode:
```
User: Clicks "Weather Expert Mode" then asks "Plan my trip"
    ↓
Terminal sends: {prompt: "Plan my trip", agent_mode: "weather"}
    ↓
MCP Wrapper: claude -p "Plan my trip" --append-system-prompt "You are a weather expert..."
    ↓
Claude: Acts as weather expert, proactively checks weather
    ↓
Response: Comprehensive weather-focused trip planning
```

### 4. Terminal Interface
The terminal should:
- Send queries as-is by default
- Optionally provide UI toggle for "expert modes"
- Let Claude decide what tools to use

### 5. Benefits of This Approach
- **Natural**: Claude behaves naturally, using tools when appropriate
- **Flexible**: Can explicitly enable expert modes when desired
- **Simple**: No complex detection logic in the frontend
- **Powerful**: Claude's intelligence decides the best approach

### 6. Testing Examples

```bash
# Natural usage (Claude decides)
"What's the weather in London?"
# Claude sees query is about weather, uses get_temperature

"Compare weather between NYC and LA"
# Claude recognizes comparison need, uses compare_weather

"I'm planning a trip to Paris"
# Claude might or might not check weather, depending on context

# With explicit weather expert mode
{agent_mode: "weather"} + "I'm planning a trip to Paris"
# Claude proactively provides weather analysis for trip planning
```

## Implementation Status

✅ MCP wrapper supports optional agent_mode
✅ Weather MCP server provides tools
✅ Terminal can send queries naturally
⏳ Test with various queries to verify behavior

## Key Insight

**Let Claude's intelligence shine!** Don't over-engineer detection logic. Claude is smart enough to:
- Understand when weather information is needed
- Use appropriate tools automatically
- Act as an expert when the context demands it

The agent_mode parameter is just an optional enhancement for when users want to explicitly invoke expert behavior.