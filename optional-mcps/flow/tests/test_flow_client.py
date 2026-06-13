from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

import httpx


FLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FLOW_DIR))

from flow_client import FlowClient, FlowConfig, extract_task_like_items  # noqa: E402


class FlowClientTests(unittest.TestCase):
    def test_list_projects_uses_api_key_header_and_get(self) -> None:
        seen: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            self.assertEqual(request.method, "GET")
            self.assertEqual(request.url.path, "/v1/projects")
            self.assertEqual(request.headers["x-flow-api-key"], "secret")
            self.assertEqual(request.url.params["page"], "1")
            self.assertEqual(request.url.params["size"], "50")
            return httpx.Response(200, json={"items": []})

        client = FlowClient(
            FlowConfig(api_key="secret"),
            transport=httpx.MockTransport(handler),
        )

        self.assertEqual(client.list_projects(), {"items": []})
        self.assertEqual(len(seen), 1)

    def test_rejects_paths_outside_read_only_prefixes(self) -> None:
        client = FlowClient(
            FlowConfig(api_key="secret"),
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})),
        )

        with self.assertRaises(ValueError):
            client.get_read_only("/v1/bots/bot-id/notifications")

    def test_search_posts_uses_keyword_and_extra_params(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.method, "GET")
            self.assertEqual(request.url.path, "/v1/search/posts")
            self.assertEqual(request.url.params["keyword"], "proposal")
            self.assertEqual(request.url.params["order"], "recent")
            return httpx.Response(200, json={"results": [{"title": "2026 proposal"}]})

        client = FlowClient(
            FlowConfig(api_key="secret"),
            transport=httpx.MockTransport(handler),
        )

        payload = client.search_posts("proposal", extra_params={"order": "recent"})
        self.assertEqual(payload["results"][0]["title"], "2026 proposal")

    def test_extract_task_like_items(self) -> None:
        payload = {
            "items": [
                {"postId": "p1", "title": "general post"},
                {"postId": "p2", "taskId": "t1", "priority": "high"},
            ]
        }

        self.assertEqual(
            extract_task_like_items(payload),
            [{"postId": "p2", "taskId": "t1", "priority": "high"}],
        )

    def test_connector_code_contains_no_write_http_verbs(self) -> None:
        forbidden = {"POST", "PATCH", "PUT", "DELETE"}
        for filename in ("flow_client.py", "server.py"):
            tree = ast.parse((FLOW_DIR / filename).read_text(encoding="utf-8"))
            constants = {
                node.value
                for node in ast.walk(tree)
                if isinstance(node, ast.Constant) and isinstance(node.value, str)
            }
            self.assertFalse(forbidden.intersection(constants), filename)


if __name__ == "__main__":
    unittest.main()
