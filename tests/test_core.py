import os
os.environ.setdefault("ALLOW_PRIVATE_TARGETS", "false")
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from falvorn.api import app
from falvorn.extract import html_to_markdown
from falvorn.security import validate_public_url, validate_url_syntax
from falvorn.models import AgentRequest


def test_health_and_docs():
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        assert client.get("/").status_code == 200
        assert client.get("/openapi.json").status_code == 200


def test_markup_extraction():
    payload = html_to_markdown("<html><head><title>Example</title><script>bad()</script></head>"
        "<body><main><h1>Heading</h1><p>Actual content</p></main></body></html>")
    assert payload["title"] == "Example"
    assert "Heading" in payload["markdown"]
    assert "bad()" not in payload["markdown"]

@pytest.mark.parametrize("url", ["file:///etc/passwd", "http://u:p@example.com", "http://example.com:1234", "javascript:alert(1)"])
def test_rejected_url_syntax(url):
    with pytest.raises(HTTPException):
        validate_url_syntax(url)

@pytest.mark.asyncio
async def test_private_ip_blocked():
    for url in ("http://127.0.0.1", "http://192.168.0.1", "http://169.254.169.254", "http://localhost"):
        with pytest.raises(HTTPException):
            await validate_public_url(url)


def test_request_validation():
    with pytest.raises(Exception):
        AgentRequest(url="https://example.com", goal="X", max_steps=100)
