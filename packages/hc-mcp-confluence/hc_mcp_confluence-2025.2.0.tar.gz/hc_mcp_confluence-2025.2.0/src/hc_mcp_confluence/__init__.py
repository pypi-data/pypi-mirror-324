import argparse
import asyncio
import sys
from . import server

def main():
    """Main entry point for the package."""
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--add-to-cline', action='store_true',
                      help='Add this server to Cline MCP settings and exit')
    parser.add_argument('--add-to-claude', action='store_true',
                      help='Add this server to Claude Desktop MCP settings and exit')
    parser.add_argument('--env', action='append', nargs=1,
                      metavar='KEY=VALUE',
                      help='Environment variable to set (can be specified multiple times)')
    args = parser.parse_args()

    # Convert env arguments to dictionary if provided
    env_vars = {}
    if args.env:
        for env_arg in args.env:
            try:
                key, value = env_arg[0].split('=', 1)
                env_vars[key] = value
            except ValueError:
                print(f"Error: Invalid environment variable format: {env_arg[0]}")
                print("Format should be: KEY=VALUE")
                sys.exit(1)

    # Handle configuration options
    if args.add_to_cline:
        server.add_to_cline_settings(env_vars)
        sys.exit(0)
    elif args.add_to_claude:
        server.add_to_claude_settings(env_vars)
        sys.exit(0)

    # Run the server normally
    asyncio.run(server.main())

__all__ = ['main', 'server']
