"""Small Python REST client for Falvorn AI. Independent of TinyFish SDK."""
from typing import Any
import httpx

class FalvornClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", api_key: str = "", timeout: float = 30):
        headers = {"X-API-Key": api_key} if api_key else {}
        self.client = httpx.Client(base_url=base_url, headers=headers, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self.client.close()

    def _call(self, method: str, route: str, payload: dict | None = None) -> Any:
        r = self.client.request(method, route, json=payload)
        r.raise_for_status()
        return r.json()

    def fetch(self, url: str, render_js: bool = False):
        return self._call("POST", "/v1/fetch", {"url": url, "render_js": render_js})

    def search(self, query: str, max_results: int = 10):
        return self._call("POST", "/v1/search", {"query": query, "max_results": max_results})

    def start_agent(self, url: str, goal: str, max_steps: int = 8):
        return self._call("POST", "/v1/agent/runs", {"url": url, "goal": goal, "max_steps": max_steps})

    def get_run(self, run_id: str):
        return self._call("GET", f"/v1/agent/runs/{run_id}")

    def monitor(self, url: str, key: str | None = None):
        return self._call("POST", "/v1/monitor/check", {"url": url, "key": key})

    def create_browser(self, url: str):
        return self._call("POST", "/v1/browser/sessions", {"url": url})

    def browser_action(self, session_id: str, action: str, **kwargs):
        return self._call("POST", f"/v1/browser/sessions/{session_id}/actions", {"action": action, **kwargs})

    def close_browser(self, session_id: str):
        return self._call("DELETE", f"/v1/browser/sessions/{session_id}")
