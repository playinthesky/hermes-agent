from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from flow_client import FlowAPIError, FlowClient, FlowConfigError


mcp = FastMCP("Flow Read-Only")


def _client() -> FlowClient:
    return FlowClient.from_env()


def _ok(data: Any) -> dict[str, Any]:
    return {"ok": True, "data": data}


def _error(exc: Exception) -> dict[str, Any]:
    if isinstance(exc, FlowAPIError):
        return {"ok": False, "error": exc.to_dict()}
    return {"ok": False, "error": {"message": str(exc), "type": type(exc).__name__}}


def _call(operation) -> dict[str, Any]:
    try:
        return _ok(operation())
    except (FlowAPIError, FlowConfigError, ValueError) as exc:
        return _error(exc)


@mcp.tool()
def flow_list_projects(
    page: int = 1,
    size: int = 50,
    participant_id: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """List Flow projects, optionally limited to projects joined by one participant."""
    return _call(
        lambda: _client().list_projects(
            page=page,
            size=size,
            participant_id=participant_id,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_list_project_participants(
    project_id: str,
    page: int = 1,
    size: int = 100,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """List members participating in one Flow project."""
    return _call(
        lambda: _client().list_project_participants(
            project_id,
            page=page,
            size=size,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_list_project_posts(
    project_id: str,
    page: int = 1,
    size: int = 20,
    include_comments: bool = False,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read recent posts from a Flow project.

    Comment data is returned when Flow includes it in the post payload.
    """
    return _call(
        lambda: _client().list_project_posts(
            project_id,
            page=page,
            size=size,
            include_comments=include_comments,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_list_project_tasks(
    project_id: str,
    page: int = 1,
    size: int = 50,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read task-like items from a Flow project's post feed without modifying task state."""
    return _call(
        lambda: _client().list_project_tasks(
            project_id,
            page=page,
            size=size,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_search_posts(
    keyword: str,
    page: int = 1,
    size: int = 20,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Search Flow posts by keyword."""
    return _call(
        lambda: _client().search_posts(
            keyword,
            page=page,
            size=size,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_search_projects(
    keyword: str,
    page: int = 1,
    size: int = 20,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Search Flow projects by keyword."""
    return _call(
        lambda: _client().search_projects(
            keyword,
            page=page,
            size=size,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_list_members(
    api_version: str = "v2",
    page: int = 1,
    size: int = 100,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """List Flow workspace members. Use api_version='v1' if the workspace has not enabled v2."""
    return _call(
        lambda: _client().list_members(
            api_version=api_version,
            page=page,
            size=size,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_list_chats(
    participant_id: str,
    page: int = 1,
    size: int = 50,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """List Flow chat rooms that a participant belongs to."""
    return _call(
        lambda: _client().list_chats(
            participant_id,
            page=page,
            size=size,
            extra_params=extra_params,
        )
    )


@mcp.tool()
def flow_get_chat(
    room_id: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read Flow chat room details."""
    return _call(lambda: _client().get_chat(room_id, extra_params=extra_params))


@mcp.tool()
def flow_get_read_only(
    path: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Advanced read-only GET for documented Flow paths.

    Allowed paths are under projects, posts, search, members, or chats.
    """
    return _call(lambda: _client().get_read_only(path, extra_params=extra_params))


if __name__ == "__main__":
    mcp.run()
