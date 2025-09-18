#!/usr/bin/env python3

def main():
    print("Hello from Python!")
    
    # Simple calculation
    result = sum(range(1, 11))
    print(f"Sum of numbers 1-10: {result}")
    
    # List comprehension example
    squares = [x**2 for x in range(1, 6)]
    print(f"Squares of 1-5: {squares}")
    
    # Dictionary example
    data = {"name": "Example", "version": "1.0", "status": "running"}
    for key, value in data.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()