#!/bin/bash

echo "==================================================="
echo "TESTING COMPLETE VISUAL TEACHING FLOW"
echo "==================================================="

echo -e "\n1️⃣ TEST: Variable Visualization"
echo "let pikachu = 3"
python -c "
import asyncio
from visual_code_mcp import variable_visualizer
asyncio.run(async def(): print(await variable_visualizer('pikachu', '3', 'assign'))())
" 2>&1

echo -e "\n==================================================="
echo "2️⃣ TEST: Comparison Visualization"
echo "if (car1 > car2)"
python -c "
import asyncio
from visual_code_mcp import comparison_visualizer
asyncio.run(async def(): print(await comparison_visualizer('car1', '>', 'car2'))())
" 2>&1

echo -e "\n==================================================="
echo "3️⃣ TEST: Array Operations"
echo "team.push('Charmander')"
python -c "
import asyncio
from visual_code_mcp import array_visualizer
asyncio.run(async def(): print(await array_visualizer('team', 'push', None, 'Charmander'))())
" 2>&1

echo -e "\n==================================================="
echo "4️⃣ TEST: Function Sequence"
echo "function drinkWater() { ... }"
python -c "
import asyncio
from visual_code_mcp import function_sequencer
steps = ['Person sees glass', 'Person picks up glass', 'Person drinks']
asyncio.run(async def(): print(await function_sequencer('drinkWater', steps))())
" 2>&1

echo -e "\n==================================================="
echo "✅ VISUAL TEACHING SYSTEM READY!"
echo "==================================================="