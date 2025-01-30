import asyncio
import argparse
import json
import os
import sys
import getpass
import base64
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

def get_cline_config_path() -> Path:
    """Determine the appropriate Cline configuration file path based on the environment.
    
    Returns:
        Path: The path to the Cline configuration file
    """
    if getpass.getuser() == 'ec2-user':
        return Path.home() / ".vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
    elif sys.platform == 'darwin':
        return Path.home() / "Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
    
    # Default to EC2 path for any other case
    return Path.home() / ".vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"

def get_claude_config_path() -> Path:
    """Determine the appropriate Claude Desktop configuration file path based on the environment.
    
    Returns:
        Path: The path to the Claude Desktop configuration file
    """
    if getpass.getuser() == 'ec2-user':
        return Path.home() / ".vscode-server/data/User/globalStorage/anthropic.claude/settings/claude_desktop_config.json"
    elif sys.platform == 'darwin':
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif sys.platform == 'win32':
        return Path(os.getenv('APPDATA', '')) / "Claude/claude_desktop_config.json"
    
    # Default to EC2 path for any other case
    return Path.home() / ".vscode-server/data/User/globalStorage/anthropic.claude/settings/claude_desktop_config.json"

from jira import JIRA
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Set logging level to WARNING by default
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize Jira client
JIRA_URL = os.getenv("JIRA_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
    raise ValueError("Missing required Jira environment variables")

jira_client = JIRA(
    server=JIRA_URL,
    basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN)
)

server = Server("hc-mcp-jira")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available Jira tools."""
    return [
        types.Tool(
            name="get_current_user",
            description="Get information about the currently authenticated user",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="create_issue",
            description="Create a new Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {"type": "string", "description": "Project key where the issue will be created"},
                    "summary": {"type": "string", "description": "Issue summary/title"},
                    "description": {"type": "string", "description": "Issue description"},
                    "issue_type": {"type": "string", "description": "Type of issue (e.g., 'Bug', 'Task', 'Story')"},
                    "priority": {"type": "string", "description": "Issue priority"},
                    "assignee": {"type": "string", "description": "Account ID of the assignee"},
                    "parent_key": {"type": "string", "description": "Parent issue key for subtasks"},
                },
                "required": ["project_key", "summary", "issue_type"],
            },
        ),
        types.Tool(
            name="update_issue",
            description="Update an existing Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Key of the issue to update"},
                    "summary": {"type": "string", "description": "New summary/title"},
                    "description": {"type": "string", "description": "New description"},
                    "status": {"type": "string", "description": "New status"},
                    "priority": {"type": "string", "description": "New priority"},
                    "assignee": {"type": "string", "description": "Account ID of the assignee"},
                    "sprint": {"type": "string", "description": "Sprint name to move the issue to"},
                },
                "required": ["issue_key"],
            },
        ),
        types.Tool(
            name="get_issue",
            description="Get complete issue details",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Issue key (e.g., PROJ-123)"},
                },
                "required": ["issue_key"],
            },
        ),
        types.Tool(
            name="search_issues",
            description="Search for issues in a project using JQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {"type": "string", "description": "Project key to search in"},
                    "jql": {"type": "string", "description": "JQL filter statement"},
                },
                "required": ["project_key", "jql"],
            },
        ),
        types.Tool(
            name="add_comment",
            description="Add a comment to a Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Key of the issue to comment on"},
                    "comment": {"type": "string", "description": "Comment text content"},
                },
                "required": ["issue_key", "comment"],
            },
        ),
        types.Tool(
            name="list_projects",
            description="List all accessible Jira projects",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Maximum number of projects to return"},
                },
            },
        ),
        types.Tool(
            name="delete_issue",
            description="Delete a Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Key of the issue to delete"},
                },
                "required": ["issue_key"],
            },
        ),
        types.Tool(
            name="create_issue_link",
            description="Create a link between two issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "inward_issue": {"type": "string", "description": "Key of the inward issue"},
                    "outward_issue": {"type": "string", "description": "Key of the outward issue"},
                    "link_type": {"type": "string", "description": "Type of link (e.g., 'blocks')"},
                },
                "required": ["inward_issue", "outward_issue", "link_type"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle Jira tool execution requests."""
    if not arguments and name != "get_current_user" and name != "list_projects":
        raise ValueError("Missing arguments")

    try:
        if name == "get_current_user":
            try:
                myself = jira_client.myself()
                # Convert JIRA Resource object to dict
                user_info = {
                    'accountId': getattr(myself, 'accountId', None),
                    'displayName': getattr(myself, 'displayName', None),
                    'emailAddress': getattr(myself, 'emailAddress', None),
                    'active': getattr(myself, 'active', None),
                    'self': getattr(myself, 'self', None),
                    'name': getattr(myself, 'name', None),
                    'key': getattr(myself, 'key', None),
                    'timeZone': getattr(myself, 'timeZone', None)
                }
                return [types.TextContent(type="text", text=json.dumps(user_info, indent=2))]
            except Exception as e:
                logger.error(f"Error getting current user: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to get current user: {str(e)}"
                    }, indent=2)
                )]

        elif name == "create_issue":
            try:
                fields = {
                    "project": {"key": arguments["project_key"]},
                    "summary": arguments["summary"],
                    "issuetype": {"name": arguments["issue_type"]},
                }
                
                if "description" in arguments:
                    fields["description"] = arguments["description"]
                if "priority" in arguments:
                    fields["priority"] = {"name": arguments["priority"]}
                if "assignee" in arguments:
                    fields["assignee"] = {"accountId": arguments["assignee"]}
                if "parent_key" in arguments:
                    fields["parent"] = {"key": arguments["parent_key"]}

                issue = jira_client.create_issue(fields=fields)
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "key": issue.key,
                        "id": issue.id,
                        "self": issue.self
                    }, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error creating issue: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to create issue: {str(e)}"
                    }, indent=2)
                )]

        elif name == "update_issue":
            try:
                issue = jira_client.issue(arguments["issue_key"])
                update_fields = {}
                updates_made = []

                if "summary" in arguments:
                    update_fields["summary"] = arguments["summary"]
                    updates_made.append("summary")
                if "description" in arguments:
                    update_fields["description"] = arguments["description"]
                    updates_made.append("description")
                if "priority" in arguments:
                    update_fields["priority"] = {"name": arguments["priority"]}
                    updates_made.append("priority")
                if "assignee" in arguments:
                    update_fields["assignee"] = {"accountId": arguments["assignee"]}
                    updates_made.append("assignee")

                if update_fields:
                    issue.update(fields=update_fields)

                if "status" in arguments:
                    transitions = jira_client.transitions(issue)
                    transition_id = None
                    for t in transitions:
                        if t["name"].lower() == arguments["status"].lower():
                            transition_id = t["id"]
                            break
                    if transition_id:
                        jira_client.transition_issue(issue, transition_id)
                        updates_made.append("status")

                if "sprint" in arguments and arguments["sprint"]:
                    sprint = arguments["sprint"]
                    # Get the project key from the issue key
                    project_key = arguments["issue_key"].split('-')[0]
                    logger.warning(f"Looking for boards for project: {project_key}")
                    
                    # Get boards for the project
                    boards = jira_client.boards(projectKeyOrID=project_key)
                    logger.warning(f"Found {len(boards)} boards for project {project_key}")
                    
                    # Look for scrum boards
                    scrum_boards = [b for b in boards if getattr(b, 'type', None) == 'scrum']
                    logger.warning(f"Found {len(scrum_boards)} scrum boards")
                    
                    sprint_found = False
                    for board in scrum_boards:
                        try:
                            # Get active and future sprints for the board
                            sprints = jira_client.sprints(board.id, state='active,future')
                            logger.warning(f"Found {len(sprints)} active/future sprints in board {board.id} - {board.name}")
                            
                            for s in sprints:
                                if s.name == sprint:
                                    logger.warning(f"Found matching sprint: {s.id} - {s.name} in board {board.name}")
                                    try:
                                        jira_client.add_issues_to_sprint(s.id, [arguments["issue_key"]])
                                        updates_made.append("sprint")
                                        sprint_found = True
                                        logger.warning("Successfully added issue to sprint")
                                        break
                                    except Exception as e:
                                        logger.error(f"Error adding issue to sprint: {e}")
                            
                            if sprint_found:
                                break
                        except Exception as e:
                            logger.warning(f"Error accessing sprints for board {board.id}: {e}")
                    
                    if not sprint_found:
                        logger.warning(f"Sprint '{sprint}' not found in any scrum board")

                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "message": f"Issue {arguments['issue_key']} updated successfully",
                        "updated_fields": updates_made,
                        "updates": update_fields
                    }, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error updating issue: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to update issue: {str(e)}"
                    }, indent=2)
                )]

        elif name == "get_issue":
            try:
                issue = jira_client.issue(arguments["issue_key"], expand='comments,attachments')
                
                comments = [{
                    "id": comment.id,
                    "author": str(comment.author),
                    "body": comment.body,
                    "created": str(comment.created)
                } for comment in issue.fields.comment.comments]
                
                attachments = [{
                    "id": attachment.id,
                    "filename": attachment.filename,
                    "size": attachment.size,
                    "created": str(attachment.created)
                } for attachment in issue.fields.attachment]
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "description": issue.fields.description,
                        "status": str(issue.fields.status),
                        "priority": str(issue.fields.priority) if hasattr(issue.fields, 'priority') else None,
                        "assignee": str(issue.fields.assignee) if hasattr(issue.fields, 'assignee') else None,
                        "type": str(issue.fields.issuetype),
                        "comments": comments,
                        "attachments": attachments
                    }, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error getting issue: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to get issue: {str(e)}"
                    }, indent=2)
                )]

        elif name == "search_issues":
            try:
                full_jql = f"project = {arguments['project_key']} AND {arguments['jql']}"
                issues = jira_client.search_issues(
                    full_jql,
                    maxResults=30,
                    fields="summary,description,status,priority,assignee,issuetype"
                )
                
                results = [{
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": str(issue.fields.status),
                    "priority": str(issue.fields.priority) if hasattr(issue.fields, 'priority') else None,
                    "assignee": str(issue.fields.assignee) if hasattr(issue.fields, 'assignee') else None,
                    "type": str(issue.fields.issuetype)
                } for issue in issues]
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error searching issues: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to search issues: {str(e)}"
                    }, indent=2)
                )]

        elif name == "add_comment":
            try:
                issue = jira_client.issue(arguments["issue_key"])
                comment = jira_client.add_comment(issue, arguments["comment"])
                result = {
                    "message": "Comment added successfully",
                    "id": comment.id
                }
                
                if "attachment" in arguments and arguments["attachment"]:
                    with NamedTemporaryFile(delete=False) as temp_file:
                        content = base64.b64decode(arguments["attachment"]["content"])
                        temp_file.write(content)
                        temp_file.flush()
                        
                        with open(temp_file.name, 'rb') as f:
                            att = jira_client.add_attachment(
                                issue=arguments["issue_key"],
                                attachment=f,
                                filename=arguments["attachment"]["filename"]
                            )
                        result["attachment_id"] = att.id
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error adding comment: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to add comment: {str(e)}"
                    }, indent=2)
                )]

        elif name == "list_projects":
            try:
                max_results = arguments.get("max_results", 50) if arguments else 50
                projects = jira_client.projects()
                project_list = [{
                    "key": project.key,
                    "name": project.name,
                    "id": project.id,
                    "projectTypeKey": project.projectTypeKey
                } for project in projects[:max_results]]
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(project_list, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error listing projects: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to list projects: {str(e)}"
                    }, indent=2)
                )]

        elif name == "delete_issue":
            try:
                issue = jira_client.issue(arguments["issue_key"])
                issue.delete()
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "message": f"Issue {arguments['issue_key']} deleted successfully"
                    }, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error deleting issue: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to delete issue: {str(e)}"
                    }, indent=2)
                )]

        elif name == "create_issue_link":
            try:
                jira_client.create_issue_link(
                    type=arguments["link_type"],
                    inwardIssue=arguments["inward_issue"],
                    outwardIssue=arguments["outward_issue"]
                )
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "message": "Issue link created successfully",
                        "link_type": arguments["link_type"],
                        "inward_issue": arguments["inward_issue"],
                        "outward_issue": arguments["outward_issue"]
                    }, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error creating issue link: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Failed to create issue link: {str(e)}"
                    }, indent=2)
                )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

def add_to_cline_settings(env_vars=None):
    """Add this server to the Cline MCP settings file.
    
    Args:
        env_vars (dict, optional): Environment variables to use. If not provided,
            will use values from current environment.
    """
    settings_path = get_cline_config_path()
    
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"mcpServers": {}}
    
    # Use provided env vars or fall back to environment variables
    env = env_vars or {
        "JIRA_URL": JIRA_URL,
        "JIRA_USERNAME": JIRA_USERNAME,
        "JIRA_API_TOKEN": JIRA_API_TOKEN
    }
    
    # Validate required environment variables
    required_vars = ["JIRA_URL", "JIRA_USERNAME", "JIRA_API_TOKEN"]
    missing_vars = [var for var in required_vars if not env.get(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Add/update server configuration
    settings["mcpServers"]["hc-mcp-jira"] = {
        "command": "uvx",
        "args": ["hc-mcp-jira"],
        "env": env,
        "disabled": True,
        "autoApprove": []
    }
    
    # Write updated settings
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"Added hc-mcp-jira server configuration to {settings_path}")

def add_to_claude_settings(env_vars=None):
    """Add this server to the Claude Desktop MCP settings file.
    
    Args:
        env_vars (dict, optional): Environment variables to use. If not provided,
            will use values from current environment.
    """
    settings_path = get_claude_config_path()
    
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {"mcpServers": {}}
    
    # Use provided env vars or fall back to environment variables
    env = env_vars or {
        "JIRA_URL": JIRA_URL,
        "JIRA_USERNAME": JIRA_USERNAME,
        "JIRA_API_TOKEN": JIRA_API_TOKEN
    }
    
    # Validate required environment variables
    required_vars = ["JIRA_URL", "JIRA_USERNAME", "JIRA_API_TOKEN"]
    missing_vars = [var for var in required_vars if not env.get(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Add/update server configuration
    settings["mcpServers"]["hc-mcp-jira"] = {
        "command": "uvx",
        "args": ["hc-mcp-jira"],
        "env": env
    }
    
    # Write updated settings
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"Added hc-mcp-jira server configuration to {settings_path}")

async def main():
    """Run the server using stdin/stdout streams."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hc-mcp-jira",
                server_version="2025.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
