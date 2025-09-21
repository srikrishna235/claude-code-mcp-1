# Scrimba Teaching MCP - Publication Success Details

## 🎉 Successfully Published
**Date:** 2025-09-21T13:59:10.857936482Z

## Registry Information

### MCP Registry
- **Name:** `io.github.Skills03/scrimba-teaching`
- **Server ID:** `db943fb5-a144-442c-8cc3-d76be306b58b`
- **Version ID:** `77461ae5-c20a-404a-a539-f453bd20b6dd`
- **Version:** `1.0.1`
- **Search URL:** https://registry.modelcontextprotocol.io/v0/servers?search=scrimba

### PyPI
- **Package Name:** `scrimba-teaching-mcp`
- **Version:** `1.0.1`
- **URL:** https://pypi.org/project/scrimba-teaching-mcp/1.0.1/

## Installation

```bash
# Install via pip
pip install scrimba-teaching-mcp

# Run the server
python -m scrimba_teaching_mcp
```

## Working Publication Command

The `mcp-publisher` tool has a bug that converts `registryType` to `registry_type`. 
Here's the working curl command that bypasses this issue:

```bash
# Get the Bearer token from ~/.mcp_publisher_token
TOKEN=$(cat ~/.mcp_publisher_token | jq -r .token)

# Make the publication request
curl -X POST "https://registry.modelcontextprotocol.io/v0/publish" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "io.github.Skills03/scrimba-teaching",
    "description": "Interactive programming teacher using Scrimba methodology for 10x retention",
    "version": "1.0.1",
    "packages": [{
      "registryType": "pypi",
      "identifier": "scrimba-teaching-mcp",
      "version": "1.0.1",
      "transport": {
        "type": "stdio"
      }
    }]
  }'
```

## Correct server.json Format

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.Skills03/scrimba-teaching",
  "description": "Interactive programming teacher using Scrimba methodology for 10x retention",
  "version": "1.0.1",
  "packages": [{
    "registryType": "pypi",
    "identifier": "scrimba-teaching-mcp",
    "version": "1.0.1",
    "transport": {
      "type": "stdio"
    }
  }]
}
```

## Authentication Process

1. **Login with GitHub:**
   ```bash
   mcp-publisher login github
   ```
   - Follow the device code authentication flow
   - Token is stored in `~/.mcp_publisher_token`

2. **Token Location:**
   - Primary: `~/.mcp_publisher_token`
   - Format: JSON with `method`, `registry`, and `token` fields

3. **Token Structure:**
   ```json
   {
     "method": "github",
     "registry": "https://registry.modelcontextprotocol.io",
     "token": "eyJhbGci..."
   }
   ```

## Key Requirements for MCP Registry

1. **PyPI Package Requirements:**
   - Must include `mcp-name` comment in README: `<!-- mcp-name: io.github.Skills03/scrimba-teaching -->`
   - Package must be published to PyPI first
   - Version in registry must match PyPI version

2. **Required Fields in Publication Request:**
   - `name`: Namespace format `io.github.USERNAME/server-name`
   - `description`: Server description
   - `version`: Root-level version (matches package version)
   - `packages`: Array with at least one package
     - `registryType`: Must be camelCase (not snake_case)
     - `identifier`: PyPI package name
     - `version`: Package version
     - `transport`: Object with `type` field (e.g., "stdio")

3. **API Endpoint:**
   - POST to `https://registry.modelcontextprotocol.io/v0/publish`
   - Requires Bearer token authentication
   - Content-Type: `application/json`

## Verification Commands

```bash
# Check if server is in registry
curl -s "https://registry.modelcontextprotocol.io/v0/servers?search=scrimba" | jq .

# Get specific server details
curl -s "https://registry.modelcontextprotocol.io/v0/servers/db943fb5-a144-442c-8cc3-d76be306b58b" | jq .

# Check PyPI package
pip show scrimba-teaching-mcp
```

## Known Issues & Solutions

### Issue: mcp-publisher converts camelCase to snake_case
**Error:** `expected required property registryType to be present`
**Solution:** Use direct curl with proper JSON instead of mcp-publisher tool

### Issue: Token expiration
**Error:** `token is expired`
**Solution:** Re-authenticate with `mcp-publisher login github`

### Issue: Missing transport field
**Error:** `invalid transport: unsupported transport type: `
**Solution:** Add `"transport": {"type": "stdio"}` to packages

## Future Updates

To publish new versions:
1. Update version in `pyproject.toml`
2. Build and upload to PyPI: `python -m build && twine upload dist/*`
3. Update version in publication JSON
4. Use the curl command above with new version number

## Support

- **GitHub Repository:** https://github.com/Skills03/claude-code-mcp
- **Issues:** https://github.com/Skills03/claude-code-mcp/issues
- **MCP Registry Docs:** https://registry.modelcontextprotocol.io/docs