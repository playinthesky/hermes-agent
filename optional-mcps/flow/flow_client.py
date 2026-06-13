from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import quote

import httpx


DEFAULT_BASE_URL = "https://api.flow.team"
DEFAULT_TIMEOUT_SECONDS = 20.0

READ_ONLY_PREFIXES = (
    "/v1/chats",
    "/v1/employees",
    "/v1/posts",
    "/v1/projects",
    "/v1/search",
    "/v2/employees",
)


class FlowConfigError(RuntimeError):
    """Raised when required Flow connector configuration is missing."""


class FlowAPIError(RuntimeError):
    """Raised for non-2xx Flow API responses."""

    def __init__(self, *, status_code: int, path: str, message: str) -> None:
        self.status_code = status_code
        self.path = path
        self.message = message
        super().__init__(f"Flow API error {status_code} for {path}: {message}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "path": self.path,
            "message": self.message,
        }


@dataclass(frozen=True)
class FlowConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "FlowConfig":
        env = os.environ if environ is None else environ
        api_key = (env.get("FLOW_API_TOKEN") or env.get("FLOW_API_KEY") or "").strip()
        if not api_key:
            raise FlowConfigError(
                "FLOW_API_TOKEN is required. FLOW_API_KEY is also accepted as an alias."
            )

        base_url = (env.get("FLOW_API_BASE_URL") or DEFAULT_BASE_URL).strip()
        raw_timeout = (env.get("FLOW_API_TIMEOUT_SECONDS") or "").strip()
        timeout_seconds = DEFAULT_TIMEOUT_SECONDS
        if raw_timeout:
            try:
                timeout_seconds = float(raw_timeout)
            except ValueError as exc:
                raise FlowConfigError("FLOW_API_TIMEOUT_SECONDS must be a number") from exc

        return cls(
            api_key=api_key,
            base_url=base_url.rstrip("/"),
            timeout_seconds=timeout_seconds,
        )


def _clean_params(params: Mapping[str, Any] | None) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in (params or {}).items():
        if value is None or value == "":
            continue
        if isinstance(value, bool):
            cleaned[key] = "true" if value else "false"
        else:
            cleaned[key] = value
    return cleaned


def _page_params(page: int | None, size: int | None) -> dict[str, int]:
    params: dict[str, int] = {}
    if page is not None:
        params["page"] = max(1, int(page))
    if size is not None:
        params["size"] = max(1, min(int(size), 100))
    return params


def _safe_id(value: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError("Flow id values cannot be empty")
    return quote(value, safe="")


def _is_task_like(item: Any) -> bool:
    if not isinstance(item, dict):
        return False
    lowered = {str(key).lower(): value for key, value in item.items()}
    type_markers = (
        "task",
        "taskid",
        "task_id",
        "taskno",
        "task_no",
        "work",
    )
    for key, value in lowered.items():
        if isinstance(value, (dict, list)):
            continue
        text = f"{key} {value}".lower()
        if any(marker in text for marker in type_markers):
            return True
    task_fields = {"priority", "worker", "assignee", "startdate", "enddate", "duedate"}
    return bool(task_fields.intersection(lowered))


def extract_task_like_items(payload: Any) -> list[dict[str, Any]]:
    """Best-effort extraction for Flow task posts from an arbitrary response."""
    found: list[dict[str, Any]] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            if _is_task_like(value):
                found.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(payload)
    return found


class FlowClient:
    """Read-only client for Flow OpenAPI."""

    def __init__(
        self,
        config: FlowConfig,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._config = config
        self._transport = transport

    @classmethod
    def from_env(cls) -> "FlowClient":
        return cls(FlowConfig.from_env())

    @property
    def base_url(self) -> str:
        return self._config.base_url

    def _headers(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "user-agent": "hermes-flow-readonly-mcp/0.1",
            "x-flow-api-key": self._config.api_key,
        }

    def _validate_read_path(self, path: str) -> str:
        path = "/" + path.lstrip("/")
        if not any(
            path == prefix or path.startswith(f"{prefix}/") for prefix in READ_ONLY_PREFIXES
        ):
            allowed = ", ".join(READ_ONLY_PREFIXES)
            raise ValueError(f"Unsupported Flow read path: {path}. Allowed prefixes: {allowed}")
        return path

    def _get(self, path: str, *, params: Mapping[str, Any] | None = None) -> Any:
        path = self._validate_read_path(path)
        url = f"{self._config.base_url}{path}"
        timeout = httpx.Timeout(self._config.timeout_seconds)
        with httpx.Client(
            headers=self._headers(),
            timeout=timeout,
            transport=self._transport,
        ) as client:
            response = client.get(url, params=_clean_params(params))

        if response.status_code < 200 or response.status_code >= 300:
            body = response.text[:1000]
            raise FlowAPIError(status_code=response.status_code, path=path, message=body)

        if response.status_code == 204 or not response.content:
            return None

        content_type = response.headers.get("content-type", "")
        if "json" in content_type.lower():
            return response.json()
        try:
            return response.json()
        except ValueError:
            return {"text": response.text}

    def list_projects(
        self,
        *,
        page: int | None = 1,
        size: int | None = 50,
        participant_id: str | None = None,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        path = "/v1/projects"
        if participant_id:
            path = f"/v1/projects/participants/{_safe_id(participant_id)}"
        return self._get(path, params={**_page_params(page, size), **_clean_params(extra_params)})

    def list_project_participants(
        self,
        project_id: str,
        *,
        page: int | None = 1,
        size: int | None = 100,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        path = f"/v1/projects/{_safe_id(project_id)}/participants"
        return self._get(path, params={**_page_params(page, size), **_clean_params(extra_params)})

    def list_project_posts(
        self,
        project_id: str,
        *,
        page: int | None = 1,
        size: int | None = 20,
        include_comments: bool = False,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        params: dict[str, Any] = {**_page_params(page, size), **_clean_params(extra_params)}
        if include_comments:
            params.setdefault("includeComments", True)
        return self._get(f"/v1/posts/projects/{_safe_id(project_id)}", params=params)

    def list_project_tasks(
        self,
        project_id: str,
        *,
        page: int | None = 1,
        size: int | None = 50,
        extra_params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self.list_project_posts(
            project_id,
            page=page,
            size=size,
            include_comments=False,
            extra_params=extra_params,
        )
        return {
            "projectId": project_id,
            "taskLikeItems": extract_task_like_items(payload),
            "raw": payload,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        page: int | None = 1,
        size: int | None = 20,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        params: dict[str, Any] = {"keyword": keyword, **_page_params(page, size)}
        params.update(_clean_params(extra_params))
        return self._get("/v1/search/posts", params=params)

    def search_projects(
        self,
        keyword: str,
        *,
        page: int | None = 1,
        size: int | None = 20,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        params: dict[str, Any] = {"keyword": keyword, **_page_params(page, size)}
        params.update(_clean_params(extra_params))
        return self._get("/v1/search/projects", params=params)

    def list_members(
        self,
        *,
        api_version: str = "v2",
        page: int | None = 1,
        size: int | None = 100,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        version = api_version.strip().lower()
        if version not in {"v1", "v2"}:
            raise ValueError("api_version must be 'v1' or 'v2'")
        return self._get(
            f"/{version}/employees",
            params={**_page_params(page, size), **_clean_params(extra_params)},
        )

    def list_chats(
        self,
        participant_id: str,
        *,
        page: int | None = 1,
        size: int | None = 50,
        extra_params: Mapping[str, Any] | None = None,
    ) -> Any:
        path = f"/v1/chats/participants/{_safe_id(participant_id)}"
        return self._get(path, params={**_page_params(page, size), **_clean_params(extra_params)})

    def get_chat(self, room_id: str, *, extra_params: Mapping[str, Any] | None = None) -> Any:
        return self._get(f"/v1/chats/{_safe_id(room_id)}", params=extra_params)

    def get_read_only(self, path: str, *, extra_params: Mapping[str, Any] | None = None) -> Any:
        return self._get(path, params=extra_params)
