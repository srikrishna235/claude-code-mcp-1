#!/usr/bin/env python3
"""
Validate server.json against MCP schema
"""

import json
import sys

def validate_server_json():
    try:
        # Import jsonschema
        import jsonschema
        import requests
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema", "requests"])
        import jsonschema
        import requests
    
    print("Fetching MCP server schema...")
    schema_url = "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json"
    schema = requests.get(schema_url).json()
    
    print("Loading server.json...")
    with open('server.json', 'r') as f:
        server_data = json.load(f)
    
    print("Validating server.json against schema...")
    try:
        jsonschema.validate(instance=server_data, schema=schema)
        print("✅ server.json is VALID!")
        print("\nServer details:")
        print(f"  Name: {server_data['name']}")
        print(f"  Version: {server_data['version']}")
        print(f"  Package: {server_data['packages'][0]['identifier']}")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Validation FAILED: {e.message}")
        print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    sys.exit(0 if validate_server_json() else 1)