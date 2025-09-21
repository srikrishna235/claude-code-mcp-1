# MCP Registry Publication Instructions

## Current Status
✅ Package successfully published to PyPI: https://pypi.org/project/scrimba-teaching-mcp/1.0.1/
⚠️ MCP Registry publication pending due to mcp-publisher tool issue

## Known Issue
The `mcp-publisher` tool (as of current version) has a bug where it converts `registryType` to `registry_type` when sending to the API, causing validation errors.

## Error Details
```
Error: publish failed: server returned status 422: 
{"title":"Unprocessable Entity","status":422,"detail":"validation failed",
"errors":[{"message":"expected required property registryType to be present"}]}
```

## Correct server.json Format
```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.Skills03/scrimba-teaching",
  "description": "Interactive programming teacher using Scrimba's methodology for 10x retention",
  "packages": [{
    "registryType": "pypi",
    "identifier": "scrimba-teaching-mcp",
    "version": "1.0.1"
  }]
}
```

## Manual Installation Instructions

### For Claude Desktop Users
1. Install via pip:
   ```bash
   pip install scrimba-teaching-mcp
   ```

2. Add to Claude Desktop config:
   ```json
   {
     "mcpServers": {
       "scrimba-teaching": {
         "command": "python",
         "args": ["-m", "scrimba_teaching_mcp"]
       }
     }
   }
   ```

### For Claude CLI Users
1. Install the package:
   ```bash
   pip install scrimba-teaching-mcp
   ```

2. Run the server:
   ```bash
   python -m scrimba_teaching_mcp
   ```

## Resolution Steps
1. Report bug to mcp-publisher repository
2. Wait for fix or try alternative publication method
3. Consider using GitHub Actions for automated registry publication

## Package Validation
- ✅ PyPI package includes `mcp-name` in README
- ✅ Package structure follows MCP standards
- ✅ Server runs successfully with FastMCP
- ✅ All teaching tools functional