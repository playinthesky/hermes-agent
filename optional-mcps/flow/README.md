# Flow Read-Only MCP for Hermes

This optional MCP lets Hermes read Flow (`flow.team`) workspace data through
the Flow OpenAPI. It is scoped to read-only access for projects, project posts,
task-like posts, search, members, and chats.

## Flow API Notes

Flow's Developer Portal is at <https://api.flow.team/docs>. The public Getting
Started page says OpenAPI requests use an API key in the `x-flow-api-key`
request header and that administrators can issue keys from the API Key
management page.

The public endpoint summaries used by this connector are:

- `GET /v1/projects`
- `GET /v1/projects/participants/{participantId}`
- `GET /v1/projects/{projectId}/participants`
- `GET /v1/posts/projects/{projectId}`
- `GET /v1/search/posts`
- `GET /v1/search/projects`
- `GET /v1/chats/participants/{participantId}`
- `GET /v1/chats/{roomId}`
- `GET /v1/employees`
- `GET /v2/employees`

Flow's public post summary does not list a standalone comment-read endpoint.
`flow_list_project_posts(..., include_comments=true)` sends
`includeComments=true`; comment data is returned when Flow includes it in the
post payload. If your logged-in Flow docs expose another documented comment
`GET`, use `flow_get_read_only` with that path.

## Security

- Put the API key only in `FLOW_API_TOKEN` or `FLOW_API_KEY`.
- Do not paste API key values into GitHub issues, chat, README examples, logs, or commits.
- This MCP never calls `POST`, `PATCH`, `PUT`, or `DELETE`.
- The advanced `flow_get_read_only` tool validates paths against read-only
  Flow prefixes before making a request.

## Local Setup

```bash
cd optional-mcps/flow
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export FLOW_API_TOKEN="...issued by Flow Developer Portal..."
.venv/bin/python server.py
```

The server speaks MCP over stdio, so it is normally launched by Hermes or
another MCP client rather than run directly in a terminal.

## Hermes Config

For a source checkout:

```yaml
mcp_servers:
  flow:
    command: /absolute/path/to/hermes-agent/optional-mcps/flow/.venv/bin/python
    args:
      - /absolute/path/to/hermes-agent/optional-mcps/flow/server.py
    enabled: true
    tools:
      include:
        - flow_list_projects
        - flow_list_project_participants
        - flow_list_project_posts
        - flow_list_project_tasks
        - flow_search_posts
        - flow_search_projects
        - flow_list_members
        - flow_list_chats
        - flow_get_chat
```

If installed through the Hermes MCP catalog after this entry is merged:

```bash
hermes mcp install flow
```

## `mcp.json` Example

```json
{
  "mcpServers": {
    "flow": {
      "command": "/absolute/path/to/hermes-agent/optional-mcps/flow/.venv/bin/python",
      "args": [
        "/absolute/path/to/hermes-agent/optional-mcps/flow/server.py"
      ],
      "env": {
        "FLOW_API_TOKEN": "${FLOW_API_TOKEN}"
      }
    }
  }
}
```

## Tools

- `flow_list_projects`
- `flow_list_project_participants`
- `flow_list_project_posts`
- `flow_list_project_tasks`
- `flow_search_posts`
- `flow_search_projects`
- `flow_list_members`
- `flow_list_chats`
- `flow_get_chat`
- `flow_get_read_only`

Most tools accept `extra_params` for Flow query parameters that are visible in
your logged-in Developer Portal but not shown in the public summary. The
connector passes those parameters only on `GET` requests.
