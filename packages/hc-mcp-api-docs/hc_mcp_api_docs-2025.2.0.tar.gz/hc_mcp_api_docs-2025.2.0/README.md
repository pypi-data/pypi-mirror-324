# HC MCP API Docs

MCP server for our API documentation. This server provides tools to interact with our API documentation system.

## Features

- List available APIs grouped by environment
- Get detailed API information including documentation URLs
- Search APIs by title and description
- Generate code examples in TypeScript, Python, and cURL

## Configuration

The server can be configured using environment variables:

- `API_DOCS_BASE_URL`: Base URL for the API documentation.

## Tools

### list_apis
List our APIs grouped by environment. Returns titles, descriptions, accounts, and stages (max 100 APIs).

### get_api_details
Get API documentation URLs, environment details, and OpenAPI spec. Returns JSON/YAML/Swagger UI links.

### search_apis
Search APIs by title/description. Prioritizes title matches. Returns max 50 sorted results.

### generate_code
Generate API client code with endpoints and error handling. Supports TypeScript, Python, cURL.

## Installation

```bash
pip install hc-mcp-api-docs
```

## Usage

The server can be used with any MCP client. Example using the Claude desktop app:

1. Add the server to your MCP configuration
2. Use the available tools through the MCP interface

## Development

```bash
# Install dependencies
make prepare

# Build package
make build

# Upload to PyPI
make upload

# Install locally
make install

# Clean build artifacts
make clean
