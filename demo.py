#!/usr/bin/env python3

def main():
    print("Hello from Python!")
    print("This is a demo Python script.")
    
    # Simple calculation
    result = 42 * 2
    print(f"42 * 2 = {result}")
    
    # List operations
    numbers = [1, 2, 3, 4, 5]
    squared = [n**2 for n in numbers]
    print(f"Original numbers: {numbers}")
    print(f"Squared numbers: {squared}")

if __name__ == "__main__":
    main()