# Multi-Tool MCP Server

## Setup
```bash
# From parent directory
echo '{"mcpServers":{"multi-tools":{"command":"python","args":["weather_mcp.py"]}}}' > .mcp.json
```

## Usage
```bash
claude "What's the weather in London?"
claude "Generate an image of a sunset"
claude "Convert this to speech: Hello world"
```

## Available Tools

### Weather
- `get_temperature(city, units)` - Get current temperature
- `get_weather_forecast(city, days)` - Get multi-day forecast  
- `compare_weather(cities)` - Compare weather between cities
Uses wttr.in API for real weather data

### AI Generation
- `generate_image(prompt)` - Generate images from text
- `text_to_speech(text)` - Convert text to speech audio
Uses FAL AI for generation