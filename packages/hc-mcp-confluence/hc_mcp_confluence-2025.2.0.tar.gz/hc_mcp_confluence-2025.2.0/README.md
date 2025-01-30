# hc-mcp-confluence

MCP server for Confluence integration. This server provides tools to interact with Confluence through the Model Context Protocol (MCP).

## Setup

1. Install the package:
```bash
pip install .
```

2. Set up environment variables:
```bash
export CONFLUENCE_URL="your-confluence-url"
export CONFLUENCE_USERNAME="your-username"
export CONFLUENCE_API_TOKEN="your-api-token"
```

## Available Tools

- `get_page`: Get content of a specific Confluence page
- `create_page`: Create a new Confluence page
- `update_page`: Update an existing Confluence page
- `delete_page`: Delete a Confluence page
- `search_content`: Search Confluence content using CQL
- `get_space`: Get details about a Confluence space
- `list_spaces`: List all Confluence spaces
- `add_page_labels`: Add labels to a Confluence page
- `get_page_labels`: Get labels of a Confluence page
- `get_page_attachments`: Get attachments of a Confluence page

## Development

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run the server:
```bash
hc-mcp-confluence
```

## Environment Variables

The following environment variables are required:

- `CONFLUENCE_URL`: The URL of your Confluence instance
- `CONFLUENCE_USERNAME`: Your Confluence username
- `CONFLUENCE_API_TOKEN`: Your Confluence API token

## Error Handling

The server includes comprehensive error handling:
- Validates required environment variables on startup
- Provides detailed error messages for API operations
- Returns formatted error responses for failed requests

## API Response Format

All tool responses are returned as text content with the following structure:
- Success: Returns the API response as a string
- Error: Returns an error message prefixed with "Error: "
