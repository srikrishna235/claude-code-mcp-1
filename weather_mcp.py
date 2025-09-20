#!/usr/bin/env python3
"""
Multi-Tool MCP Server - Weather, Teaching, and Image Generation
Provides various tools to Claude Code
"""

import asyncio
import httpx
import json
from typing import Optional, Dict
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Initialize MCP server
mcp = FastMCP("multi-tools")

@mcp.tool()
async def get_temperature(
    city: str,
    units: Optional[str] = "celsius"
) -> str:
    """
    Get current temperature for a city.
    
    Args:
        city: Name of the city (e.g., "London", "New York")
        units: Temperature units - "celsius" or "fahrenheit" (default: celsius)
    
    Returns:
        Current temperature and weather conditions
    """
    try:
        # Use wttr.in API - free and no key required
        # Format: m for metric (celsius), u for USCS (fahrenheit)
        unit_param = "m" if units.lower() == "celsius" else "u"
        
        # Parameters: format=j1 for JSON, m/u for units
        url = f"https://wttr.in/{city}?format=j1&{unit_param}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract current conditions
                current = data.get('current_condition', [{}])[0]
                temp = current.get('temp_C' if unit_param == 'm' else 'temp_F', 'Unknown')
                feels_like = current.get('FeelsLikeC' if unit_param == 'm' else 'FeelsLikeF', 'Unknown')
                weather = current.get('weatherDesc', [{}])[0].get('value', 'Unknown')
                humidity = current.get('humidity', 'Unknown')
                wind_speed = current.get('windspeedKmph' if unit_param == 'm' else 'windspeedMiles', 'Unknown')
                
                unit_symbol = "°C" if units.lower() == "celsius" else "°F"
                speed_unit = "km/h" if unit_param == 'm' else "mph"
                
                result = f"""Weather in {city}:
🌡️ Temperature: {temp}{unit_symbol}
🤔 Feels like: {feels_like}{unit_symbol}
☁️ Conditions: {weather}
💧 Humidity: {humidity}%
💨 Wind: {wind_speed} {speed_unit}"""
                
                return result
            else:
                return f"Error: Could not fetch weather for {city}. Status: {response.status_code}"
                
    except httpx.TimeoutException:
        return f"Error: Request timed out while fetching weather for {city}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

@mcp.tool()
async def get_weather_forecast(
    city: str,
    days: Optional[int] = 3
) -> str:
    """
    Get weather forecast for a city.
    
    Args:
        city: Name of the city
        days: Number of days to forecast (1-3, default: 3)
    
    Returns:
        Weather forecast for the specified days
    """
    try:
        # Limit days to 1-3 (free API limit)
        days = min(max(days, 1), 3)
        
        url = f"https://wttr.in/{city}?format=j1&m"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = data.get('weather', [])
                
                forecast = f"📅 {days}-Day Forecast for {city}:\n\n"
                
                for i, day_weather in enumerate(weather_data[:days]):
                    date = day_weather.get('date', 'Unknown')
                    max_temp = day_weather.get('maxtempC', 'Unknown')
                    min_temp = day_weather.get('mintempC', 'Unknown')
                    
                    # Get average description from hourly data
                    hourly = day_weather.get('hourly', [])
                    if hourly and len(hourly) > 4:  # Get midday weather
                        midday = hourly[4]  # Around noon
                        desc = midday.get('weatherDesc', [{}])[0].get('value', 'Unknown')
                        rain_chance = midday.get('chanceofrain', '0')
                    else:
                        desc = "Unknown"
                        rain_chance = "0"
                    
                    forecast += f"""Day {i+1} ({date}):
  🌡️ High: {max_temp}°C, Low: {min_temp}°C
  ☁️ {desc}
  ☔ Rain chance: {rain_chance}%\n\n"""
                
                return forecast.strip()
            else:
                return f"Error: Could not fetch forecast for {city}"
                
    except Exception as e:
        return f"Error fetching forecast: {str(e)}"

@mcp.tool()
async def compare_weather(
    cities: str
) -> str:
    """
    Compare weather between multiple cities.
    
    Args:
        cities: Comma-separated list of cities (e.g., "London,Paris,Tokyo")
    
    Returns:
        Weather comparison table
    """
    try:
        city_list = [c.strip() for c in cities.split(',')][:5]  # Limit to 5 cities
        
        results = []
        async with httpx.AsyncClient() as client:
            for city in city_list:
                url = f"https://wttr.in/{city}?format=j1&m"
                response = await client.get(url, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    current = data.get('current_condition', [{}])[0]
                    temp = current.get('temp_C', 'N/A')
                    weather = current.get('weatherDesc', [{}])[0].get('value', 'Unknown')
                    humidity = current.get('humidity', 'N/A')
                    
                    results.append({
                        'city': city,
                        'temp': temp,
                        'weather': weather,
                        'humidity': humidity
                    })
                else:
                    results.append({
                        'city': city,
                        'temp': 'Error',
                        'weather': 'Failed to fetch',
                        'humidity': 'N/A'
                    })
        
        # Format as comparison table
        comparison = "🌍 Weather Comparison:\n\n"
        comparison += f"{'City':<15} {'Temp':<8} {'Conditions':<20} {'Humidity':<10}\n"
        comparison += "-" * 55 + "\n"
        
        for r in results:
            comparison += f"{r['city']:<15} {r['temp']:>6}°C  {r['weather']:<20} {r['humidity']:>6}%\n"
        
        return comparison
        
    except Exception as e:
        return f"Error comparing weather: {str(e)}"

@mcp.tool()
async def generate_image(
    prompt: str
) -> str:
    """
    Generate an image from a text prompt using FAL AI.
    
    Args:
        prompt: Text description of the image to generate
    
    Returns:
        Prompt and URL of the generated image
    """
    try:
        import os
        import fal_client
        
        # Set API key
        os.environ["FAL_KEY"] = "3845a313-cfc9-469b-ac5d-fe354d7106dd:42f4fb3cddc5156df1b724115431bb85"
        
        # Run in async executor since fal_client.subscribe is sync
        import concurrent.futures
        
        def generate():
            result = fal_client.subscribe(
                "fal-ai/qwen-image",
                arguments={"prompt": prompt},
                with_logs=False
            )
            return result
        
        # Run in thread executor
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, generate)
        
        if result and "images" in result:
            url = result["images"][0]["url"]
            return f"Prompt: {prompt}\nURL: {url}"
        return "Error: No image generated"
            
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def text_to_speech(
    text: str
) -> str:
    """
    Generate speech audio from text.
    
    Args:
        text: Text to convert to speech
    
    Returns:
        Text and URL of the generated audio
    """
    try:
        import os
        import fal_client
        
        # Set API key
        os.environ["FAL_KEY"] = "3845a313-cfc9-469b-ac5d-fe354d7106dd:42f4fb3cddc5156df1b724115431bb85"
        
        # Run in async executor since fal_client.subscribe is sync
        import concurrent.futures
        
        def generate():
            result = fal_client.subscribe(
                "fal-ai/chatterbox/text-to-speech",
                arguments={"text": text},
                with_logs=False
            )
            return result
        
        # Run in thread executor
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, generate)
        
        if result and "audio" in result:
            url = result["audio"]["url"]
            return f"Text: {text}\nAudio URL: {url}"
        return "Error: No audio generated"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Create app with CORS support
def create_app():
    """Create Starlette app with CORS and MCP mounted"""
    app = Starlette()
    
    # Add CORS middleware for browser access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

# Run server
async def run_server(host="127.0.0.1", port=8003):
    """Run the weather MCP server"""
    app = create_app()
    
    # Get the MCP ASGI app and mount it
    mcp_app = mcp.streamable_http_app()
    app.mount("/", mcp_app)
    
    # Run with session manager
    async with mcp.session_manager.run():
        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

# Run the server
if __name__ == "__main__":
    import sys
    
    # Check if running in stdio mode (default for Claude MCP)
    if "--http" in sys.argv:
        # HTTP mode for direct testing
        print("Multi-Tool MCP Server (HTTP Mode)")
        print("==================================")
        print("Starting server on http://localhost:8003")
        print("")
        print("Available tools:")
        print("  - get_temperature: Get current temperature for a city")
        print("  - get_weather_forecast: Get multi-day forecast")
        print("  - compare_weather: Compare weather between cities")
        print("  - generate_image: Generate AI images from text prompts")
        print("  - text_to_speech: Convert text to speech audio")
        print("")
        
        # Run HTTP server
        asyncio.run(run_server())
    else:
        # STDIO mode for Claude Code integration
        # This is what Claude Code expects when running as subprocess
        mcp.run()  # Default is stdio transport