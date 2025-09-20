# Weather MCP Tool

## Setup
```bash
# From parent directory
echo '{"mcpServers":{"weather-tools":{"command":"python","args":["weather_mcp.py"]}}}' > .mcp.json
```

## Usage
```bash
claude "What's the weather in London?"
```

## Available Tools
- get_temperature(city, units)
- get_weather_forecast(city, days)
- compare_weather(cities)

Uses real wttr.in API for weather data.