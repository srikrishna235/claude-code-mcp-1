# Weather Tools for Claude Code

## What We Built

A custom MCP server that provides weather tools to Claude Code:
- **get_temperature**: Get current weather for any city
- **get_weather_forecast**: Get 1-3 day forecast
- **compare_weather**: Compare weather between multiple cities

## How It Works

```
Claude Code → MCP Protocol → Weather Server → wttr.in API → Weather Data
```

## Running the Weather Server

```bash
# Start the weather MCP server
python3 weather_mcp.py

# Server runs on http://localhost:8003
```

## Connecting to Claude Code

### Method 1: Direct HTTP Connection
```bash
# Add as HTTP MCP server
claude mcp add weather http://localhost:8003
```

### Method 2: As Subprocess
```bash
# Add as subprocess MCP server
claude mcp add weather "python3 /path/to/weather_mcp.py"
```

## Using the Weather Tools

Once connected, Claude Code can use these tools automatically:

```bash
# Ask Claude about weather
claude "What's the weather in London?"
# Claude will use get_temperature tool

claude "Give me a 3-day forecast for Tokyo"
# Claude will use get_weather_forecast tool

claude "Compare weather between NYC, Paris, and Sydney"
# Claude will use compare_weather tool
```

## Example Results

### Get Temperature
```
Weather in London:
🌡️ Temperature: 16°C
🤔 Feels like: 16°C
☁️ Conditions: Partly cloudy
💧 Humidity: 88%
💨 Wind: 5 km/h
```

### Weather Forecast
```
📅 3-Day Forecast for Tokyo:

Day 1 (2025-09-20):
  🌡️ High: 26°C, Low: 25°C
  ☁️ Patchy rain nearby
  ☔ Rain chance: 100%
```

### Compare Cities
```
🌍 Weather Comparison:

City            Temp     Conditions           Humidity  
-------------------------------------------------------
New York            23°C  Partly cloudy            38%
Paris               21°C  Patchy rain nearby       64%
Sydney              20°C  Sunny                    49%
```

## Technical Details

### Tool Parameters

**get_temperature**:
- `city`: City name (required)
- `units`: "celsius" or "fahrenheit" (default: celsius)

**get_weather_forecast**:
- `city`: City name (required)
- `days`: 1-3 days (default: 3)

**compare_weather**:
- `cities`: Comma-separated city names (max 5)

### API Used
- **wttr.in**: Free weather API, no key required
- Rate limits apply for heavy usage
- Supports worldwide cities

## How to Create Your Own Tools

1. **Define the tool with @mcp.tool() decorator**
2. **Add parameters with type hints**
3. **Return string results**
4. **Run as MCP server**

Example template:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
async def my_custom_tool(param1: str, param2: int = 10) -> str:
    """Tool description for Claude"""
    # Your logic here
    return "Result"
```

## Key Learnings

1. **MCP is the standard** for extending Claude Code with custom tools
2. **Tools are just Python functions** with the @mcp.tool() decorator
3. **Claude decides when to use tools** based on user queries
4. **No API keys needed** for wttr.in weather data
5. **FastMCP handles the protocol** - you just write functions

## Next Steps

- Add more weather details (UV index, sunrise/sunset)
- Cache results to reduce API calls
- Add weather alerts/warnings
- Support location coordinates
- Add historical weather data

## Summary

This demonstrates how to:
1. **Create custom tools** for Claude Code
2. **Wrap external APIs** as MCP tools
3. **Run MCP servers** independently
4. **Connect tools** to Claude Code

The weather tools are now available to Claude Code whenever you ask about weather!