#!/usr/bin/env python3
import json
import logging
import os
import sys
import getpass
from pathlib import Path

def get_cline_config_path() -> Path:
    """Determine the appropriate Cline configuration file path based on the environment."""
    if getpass.getuser() == 'ec2-user':
        return Path.home() / ".vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
    elif sys.platform == 'darwin':
        return Path.home() / "Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
    
    # Default to EC2 path for any other case
    return Path.home() / ".vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"

def get_claude_config_path() -> Path:
    """Determine the appropriate Claude Desktop configuration file path based on the environment."""
    if getpass.getuser() == 'ec2-user':
        return Path.home() / ".vscode-server/data/User/globalStorage/anthropic.claude/settings/claude_desktop_config.json"
    elif sys.platform == 'darwin':
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif sys.platform == 'win32':
        return Path(os.getenv('APPDATA', '')) / "Claude/claude_desktop_config.json"
    
    # Default to EC2 path for any other case
    return Path.home() / ".vscode-server/data/User/globalStorage/anthropic.claude/settings/claude_desktop_config.json"

def add_to_cline_settings(env_vars=None):
    """Add this server to the Cline MCP settings file."""
    settings_path = get_cline_config_path()
    
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"mcpServers": {}}
    
    # Use provided env vars or fall back to environment variables
    env = env_vars or {
        "API_DOCS_BASE_URL": os.getenv('API_DOCS_BASE_URL')
    }
    
    # Validate required environment variables
    if not env.get("API_DOCS_BASE_URL"):
        print("Error: Missing required environment variable: API_DOCS_BASE_URL")
        sys.exit(1)
    
    # Add/update server configuration
    settings["mcpServers"]["hc-mcp-api-docs"] = {
        "command": "uvx",
        "args": ["hc-mcp-api-docs"],
        "env": env,
        "disabled": False,
        "autoApprove": []
    }
    
    # Write updated settings
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"Added hc-mcp-api-docs server configuration to {settings_path}")

def add_to_claude_settings(env_vars=None):
    """Add this server to the Claude Desktop MCP settings file."""
    settings_path = get_claude_config_path()
    
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"mcpServers": {}}
    
    # Use provided env vars or fall back to environment variables
    env = env_vars or {
        "API_DOCS_BASE_URL": os.getenv('API_DOCS_BASE_URL')
    }
    
    # Validate required environment variables
    if not env.get("API_DOCS_BASE_URL"):
        print("Error: Missing required environment variable: API_DOCS_BASE_URL")
        sys.exit(1)
    
    # Add/update server configuration
    settings["mcpServers"]["hc-mcp-api-docs"] = {
        "command": "uvx",
        "args": ["hc-mcp-api-docs"],
        "env": env
    }
    
    # Write updated settings
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"Added hc-mcp-api-docs server configuration to {settings_path}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os
from typing import Dict, List, Optional, TypedDict
from urllib.parse import urljoin
from pydantic import Field
from mcp.server.fastmcp import FastMCP
import httpx

# Base URL for API documentation from environment variable
API_DOCS_BASE_URL = os.getenv('API_DOCS_BASE_URL')
if not API_DOCS_BASE_URL:
    logger.error("API_DOCS_BASE_URL environment variable is not set")
    sys.exit(1)

class ApiSpec(TypedDict):
    environment: str
    account: str
    accountName: str
    region: str
    apiId: str
    stage: str
    title: str
    description: str
    swaggerFileJSON: str
    swaggerFileYAML: str
    swaggerUIUrl: str
    spec: Optional[Dict]

class ApiDocsServer:
    """Our API documentation can be found from this server"""
    def __init__(self):
        self.mcp = FastMCP("API Documentation Server")
        self.api_specs: List[ApiSpec] = []
        self._setup_tool_handlers()

    def _setup_tool_handlers(self):
        @self.mcp.tool()
        def list_apis(
            environment: Optional[str] = Field(description="Filter environment (development/test/accept/production). Default: None", default="None")
        ) -> Dict:
            """List our APIs grouped by environment. Returns titles, descriptions, accounts, and stages (max 100 APIs)."""
            self._load_api_specs_sync()

            apis = self.api_specs
            if environment:
                apis = [api for api in apis if api["environment"] == environment]

            # Group APIs by environment
            grouped_apis = {}
            for api in apis:
                env = api["environment"]
                if env not in grouped_apis:
                    grouped_apis[env] = []
                grouped_apis[env].append(api)

            result = "Available APIs:\n\n"
            for env in sorted(grouped_apis.keys()):
                result += f"Environment: {env}\n"
                for api in sorted(grouped_apis[env], key=lambda x: x["title"]):
                    result += f"- {api['title']}"
                    if api["description"]:
                        result += f": {api['description']}"
                    result += f"\n  Account: {api['accountName']} ({api['account']})"
                    result += f"\n  Stage: {api['stage']}"
                    result += "\n\n"
                result += "\n"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }

        @self.mcp.tool()
        def get_api_details(
            api_title: str = Field(description="Exact API title to retrieve"),
            environment: Optional[str] = Field(description="Filter environment (development/test/accept/production). Default: None", default=None),
            include_spec: bool = Field(description="Include OpenAPI specification. Default: False", default=False)
        ) -> Dict:
            """Get API documentation URLs, environment details, and OpenAPI spec. Returns JSON/YAML/Swagger UI links."""
            self._load_api_specs_sync()

            # Find matching APIs
            matches = []
            for api in self.api_specs:
                if api["title"] == api_title:
                    if not environment or api["environment"] == environment:
                        matches.append(api)

            if not matches:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"No API found with title: {api_title}"
                        }
                    ]
                }

            result = ""
            for api in matches:
                result += f"API: {api['title']}\n"
                result += f"Environment: {api['environment']}\n"
                result += f"Account: {api['accountName']} ({api['account']})\n"
                result += f"Region: {api['region']}\n"
                result += f"Stage: {api['stage']}\n"
                if api["description"]:
                    result += f"\nDescription:\n{api['description']}\n"
                
                # Add full URLs
                json_url = urljoin(API_DOCS_BASE_URL, api['swaggerFileJSON'])
                yaml_url = urljoin(API_DOCS_BASE_URL, api['swaggerFileYAML'])
                swagger_url = urljoin(API_DOCS_BASE_URL, api['swaggerUIUrl'])
                
                result += f"\nDocumentation:\n"
                result += f"- JSON: {json_url}\n"
                result += f"- YAML: {yaml_url}\n"
                result += f"- Swagger UI: {swagger_url}\n"

                if include_spec:
                    try:
                        spec_response = httpx.get(json_url, timeout=30.0)
                        spec_response.raise_for_status()
                        spec = spec_response.json()
                        result += f"\nAPI Specification:\n"
                        result += json.dumps(spec, indent=2)
                    except Exception as e:
                        result += f"\nError loading specification: {e}\n"

                result += "\n---\n\n"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }

        @self.mcp.tool()
        def search_apis(
            query: str = Field(description="Search term in titles/descriptions (max 100 chars)"),
            environment: Optional[str] = Field(description="Filter environment (development/test/accept/production). Default: None", default=None)
        ) -> Dict:
            """Search APIs by title/description. Prioritizes title matches. Returns max 50 sorted results."""
            if not query:
                return {"error": "Search query is required"}

            self._load_api_specs_sync()

            # Filter by environment if specified
            apis = self.api_specs
            if environment:
                apis = [api for api in apis if api["environment"] == environment]

            # Simple text matching search
            query = query.lower()
            matches = []
            for api in apis:
                score = 0
                if query in api["title"].lower():
                    score += 3
                if query in api["description"].lower():
                    score += 2
                
                if score > 0:
                    matches.append({
                        "title": api["title"],
                        "description": api["description"],
                        "environment": api["environment"],
                        "score": score
                    })

            # Sort by score
            matches.sort(key=lambda x: x["score"], reverse=True)

            result = "Found APIs:\n\n"
            for match in matches:
                result += f"- {match['title']} ({match['environment']})\n"
                if match["description"]:
                    result += f"  {match['description']}\n"
                result += "\n"

            if not matches:
                result = "No matching APIs found."

            return {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }

        @self.mcp.tool()
        def generate_code(
            api_title: str = Field(description="Exact API title to generate code for"),
            environment: str = Field(description="Target environment (development/test/accept/production)"),
            language: str = Field(description="Code language (typescript/python/curl)")
        ) -> Dict:
            """Generate API client code with endpoints and error handling. Supports TypeScript, Python, cURL."""
            if not all([api_title, environment, language]):
                return {"error": "API title, environment, and language are required"}

            if language not in ["typescript", "python", "curl"]:
                return {"error": "Language must be one of: typescript, python, curl"}

            self._load_api_specs_sync()

            # Find the API
            api = next((api for api in self.api_specs 
                       if api["title"] == api_title and api["environment"] == environment), None)
            
            if not api:
                return {"error": f"API not found: {api_title} in {environment}"}

            # Get full URLs
            json_url = urljoin(API_DOCS_BASE_URL, api['swaggerFileJSON'])
            yaml_url = urljoin(API_DOCS_BASE_URL, api['swaggerFileYAML'])
            swagger_url = urljoin(API_DOCS_BASE_URL, api['swaggerUIUrl'])

            # Try to get the OpenAPI spec
            try:
                spec_response = httpx.get(json_url, timeout=30.0)
                spec_response.raise_for_status()
                spec = spec_response.json()
                
                # Get server URL from spec if available
                server_url = spec.get('servers', [{'url': 'API_BASE_URL'}])[0]['url']
                
                # Get available endpoints
                paths = spec.get('paths', {})
                endpoints = []
                for path, methods in paths.items():
                    for method in methods:
                        endpoints.append(f"{method.upper()} {path}")
            except Exception as e:
                server_url = "API_BASE_URL"
                endpoints = ["# Failed to load API specification"]

            # Generate code using templates
            if language == "python":
                code = f"""import httpx

# API Documentation:
# JSON: {json_url}
# YAML: {yaml_url}
# Swagger UI: {swagger_url}

async def call_{api_title.lower()}_api():
    base_url = "{server_url}"
    
    # Available endpoints:
{chr(10).join('    # ' + endpoint for endpoint in endpoints)}
    
    # Example request:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{{base_url}}/your-endpoint")
        response.raise_for_status()
        return response.json()
"""
            elif language == "typescript":
                code = f"""// API Documentation:
// JSON: {json_url}
// YAML: {yaml_url}
// Swagger UI: {swagger_url}

async function call{api_title}Api() {{
    const baseUrl = "{server_url}";
    
    // Available endpoints:
{chr(10).join('    // ' + endpoint for endpoint in endpoints)}
    
    // Example request:
    const response = await fetch(`${{baseUrl}}/your-endpoint`);
    if (!response.ok) throw new Error(`HTTP error! status: ${{response.status}}`);
    return response.json();
}}
"""
            else:  # curl
                code = f"""# API Documentation:
# JSON: {json_url}
# YAML: {yaml_url}
# Swagger UI: {swagger_url}

# Base URL: {server_url}

# Available endpoints:
{chr(10).join('# ' + endpoint for endpoint in endpoints)}

# Example request:
curl -X GET "{server_url}/your-endpoint"
"""

            return {
                "content": [
                    {
                        "type": "text",
                        "text": code
                    }
                ]
            }

    def _load_api_specs_sync(self):
        if self.api_specs:
            return

        try:
            if not API_DOCS_BASE_URL:
                logger.error("Cannot load API specs: API_DOCS_BASE_URL is not set")
                return

            # Load and parse the index file from the API documentation URL
            # Construct the URL
            index_url = urljoin(API_DOCS_BASE_URL, "index.json")
            logger.info(f"Attempting to load API specs from: {index_url}")

            # Fetch and parse the data
            try:
                response = httpx.get(index_url, timeout=30.0)
                response.raise_for_status()
                self.api_specs = response.json()
                logger.info(f"Successfully loaded {len(self.api_specs)} API specs")
            except httpx.HTTPError as e:
                logger.error(f"HTTP error while fetching API specs: {e}")
                self.api_specs = []
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse API specs JSON: {e}")
                self.api_specs = []
            except Exception as e:
                logger.error(f"Unexpected error while loading API specs: {e}")
                self.api_specs = []

        except Exception as e:
            logger.error(f"Critical error in _load_api_specs_sync: {e}")
            self.api_specs = []

    def run(self):
        """Run the MCP server"""
        self.mcp.run()

if __name__ == "__main__":
    import sys

    server = ApiDocsServer()
    try:
        server.run()
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)
