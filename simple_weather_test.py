#!/usr/bin/env python3
"""
Simple test to run weather tools directly
"""
import asyncio
from weather_mcp import get_temperature, get_weather_forecast, compare_weather

async def test():
    print("Testing weather tools directly:\n")
    
    # Test 1: Get temperature
    result = await get_temperature("London")
    print("London weather:")
    print(result)
    print()
    
    # Test 2: Get forecast
    result = await get_weather_forecast("Tokyo", days=2)
    print("Tokyo forecast:")
    print(result)
    print()
    
    # Test 3: Compare cities
    result = await compare_weather("New York,Paris,Sydney")
    print("City comparison:")
    print(result)

asyncio.run(test())
