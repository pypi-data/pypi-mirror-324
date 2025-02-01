import json
import os
import base64
import logging
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional

from jira import JIRA
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from . import REQUIRED_ENV_VARS

# Set logging level to WARNING by default
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

server = Server("hc-mcp-jira")

def initialize_jira_client() -> JIRA:
    """Initialize and return JIRA client using environment variables.
    
    Raises:
        ValueError: If required environment variables are missing
    """
    env_vars = {var: os.getenv(var) for var in REQUIRED_ENV_VARS}
    if not all(env_vars.values()):
        raise ValueError(f"Missing required environment variables: {[var for var in REQUIRED_ENV_VARS if not env_vars[var]]}")
    
    return JIRA(
        server=env_vars["JIRA_URL"],
        basic_auth=(env_vars["JIRA_USERNAME"], env_vars["JIRA_API_TOKEN"])
    )

# Initialize Jira client
jira_client = initialize_jira_client()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available Jira tools."""
    return [
        types.Tool(
            name="get_current_user",
            description="Get detailed information about the currently authenticated Jira user including account ID, display name, email, timezone, and active status. Returns a structured JSON response with all available user details.",
            inputSchema={
                "type": "object",
                "properties": {},
                "description": "No parameters required"
            },
        ),
        types.Tool(
            name="create_issue",
            description="Create a new Jira issue with specified details. Returns a JSON response containing the created issue's key, ID, and self URL. Supports creating subtasks by providing a parent issue key.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {"type": "string", "description": "Project key where the issue will be created (e.g., 'PROJ')"},
                    "summary": {"type": "string", "description": "Issue summary/title - should be clear and concise"},
                    "description": {"type": "string", "description": "Detailed description of the issue in plain text"},
                    "issue_type": {"type": "string", "description": "Type of issue. Common values: 'Bug', 'Task', 'Story', 'Sub-task'"},
                    "priority": {"type": "string", "description": "Issue priority level (e.g., 'High', 'Medium', 'Low')"},
                    "assignee": {"type": "string", "description": "Account ID of the user to assign the issue to"},
                    "parent_key": {"type": "string", "description": "Key of parent issue when creating subtasks (e.g., 'PROJ-123')"},
                },
                "required": ["project_key", "summary", "issue_type"],
                "description": "Create issue with required fields, optionally set description, priority, assignee, or parent for subtasks"
            },
        ),
        types.Tool(
            name="update_issue",
            description="Update an existing Jira issue with new field values. Supports updating basic fields, changing status through transitions, and moving issues between sprints. Returns a JSON response detailing all successful updates.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Key of the issue to update (e.g., 'PROJ-123')"},
                    "summary": {"type": "string", "description": "New summary/title for the issue"},
                    "description": {"type": "string", "description": "New description text for the issue"},
                    "status": {"type": "string", "description": "New status to transition the issue to (e.g., 'In Progress', 'Done')"},
                    "priority": {"type": "string", "description": "New priority level for the issue"},
                    "assignee": {"type": "string", "description": "Account ID of the new assignee"},
                    "sprint": {"type": "string", "description": "Name of the sprint to move the issue to (searches active and future sprints)"},
                },
                "required": ["issue_key"],
                "description": "Provide issue_key and any fields to update. Status changes use available transitions. Sprint changes search all scrum boards."
            },
        ),
        types.Tool(
            name="get_issue",
            description="Retrieve comprehensive details about a Jira issue including its fields, comments, and attachments. Returns a structured JSON response containing all issue information, comment history, and attachment metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Issue key to retrieve details for (e.g., 'PROJ-123')"},
                },
                "required": ["issue_key"],
                "description": "Provide the issue key to get full details including comments and attachments"
            },
        ),
        types.Tool(
            name="search_issues",
            description="Search for issues in a project using JQL (Jira Query Language). Returns a JSON array of matching issues with key details. Limited to 30 results per query. Results include summary, status, priority, assignee, and issue type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {"type": "string", "description": "Project key to search in (e.g., 'PROJ')"},
                    "jql": {"type": "string", "description": "JQL filter statement (e.g., 'status = \"In Progress\" AND assignee = currentUser()')"},
                },
                "required": ["project_key", "jql"],
                "description": "Combines project_key with JQL for searching. JQL supports complex queries with AND, OR, ORDER BY"
            },
        ),
        types.Tool(
            name="add_comment",
            description="Add a comment to a Jira issue with optional file attachment support. Returns a JSON response with the comment ID and attachment details if provided. Attachments are handled securely using base64 encoding.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Key of the issue to comment on (e.g., 'PROJ-123')"},
                    "comment": {"type": "string", "description": "Text content of the comment to add"},
                    "attachment": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Name of the file to attach"},
                            "content": {"type": "string", "description": "Base64 encoded file content"}
                        },
                        "description": "Optional file attachment details"
                    }
                },
                "required": ["issue_key", "comment"],
                "description": "Provide issue_key and comment text. Optionally include attachment with filename and base64 content"
            },
        ),
        types.Tool(
            name="list_projects",
            description="List all Jira projects accessible to the authenticated user. Returns a JSON array of projects with key details including project key, name, ID, and type. Results can be limited to control response size.",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Maximum number of projects to return (default: 50)"},
                },
                "description": "Optionally specify max_results to limit the number of projects returned"
            },
        ),
        types.Tool(
            name="delete_issue",
            description="Permanently delete a Jira issue or subtask. Returns a JSON confirmation response. Use with caution as this action cannot be undone.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {"type": "string", "description": "Key of the issue to delete (e.g., 'PROJ-123')"},
                },
                "required": ["issue_key"],
                "description": "Provide the issue key to permanently delete. Warning: This action is irreversible"
            },
        ),
        types.Tool(
            name="create_issue_link",
            description="Create a relationship link between two Jira issues. Returns a JSON confirmation response. Common link types include 'blocks', 'is blocked by', 'relates to', 'duplicates', 'is duplicated by'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "inward_issue": {"type": "string", "description": "Key of the inward issue (e.g., 'PROJ-123')"},
                    "outward_issue": {"type": "string", "description": "Key of the outward issue (e.g., 'PROJ-456')"},
                    "link_type": {"type": "string", "description": "Type of relationship link (e.g., 'blocks', 'relates to')"},
                },
                "required": ["inward_issue", "outward_issue", "link_type"],
                "description": "Specify both issue keys and the type of relationship to create between them"
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

from . import __version__ as VERSION

async def main():
    """Run the server using stdin/stdout streams."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hc-mcp-jira",
                server_version=VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
