"""MCP server for Jira integration."""
import argparse
import asyncio
import sys
from typing import Dict, List, Optional
from mcp_config_manager import add_to_config  # From published package

__version__ = "2025.3.5"  # Keep in sync with pyproject.toml

# Define required environment variables
REQUIRED_ENV_VARS: List[str] = ["JIRA_URL", "JIRA_USERNAME", "JIRA_API_TOKEN"]

from . import server

def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description="MCP server for Jira integration")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--add-to-cline', action='store_true',
                      help='Add this server to Cline MCP settings and exit')
    parser.add_argument('--add-to-claude', action='store_true',
                      help='Add this server to Claude Desktop MCP settings and exit')
    parser.add_argument('--env', action='append', nargs=1,
                      metavar='KEY=VALUE',
                      help='Environment variable to set (can be specified multiple times)')
    parser.add_argument('--envs', action='store_true',
                      help='Print required environment variables and exit')
    args = parser.parse_args()

    # Print required environment variables if requested
    if args.envs:
        print("Required environment variables:")
        for var in REQUIRED_ENV_VARS:
            print(f"- {var}")
        sys.exit(0)

    # Convert env arguments to dictionary if provided
    env_vars: Optional[Dict[str, str]] = None
    if args.env:
        env_vars = {}
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
        add_to_config(
            server_name="hc-mcp-jira",
            required_env_vars=REQUIRED_ENV_VARS,
            env_vars=env_vars,
            config_type="cline"
        )
        sys.exit(0)
    elif args.add_to_claude:
        add_to_config(
            server_name="hc-mcp-jira",
            required_env_vars=REQUIRED_ENV_VARS,
            env_vars=env_vars,
            config_type="claude"
        )
        sys.exit(0)

    # Run the server normally
    asyncio.run(server.main())

__all__ = ['main', 'server']
