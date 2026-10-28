"""Basic egress safety. Production requires network-level egress controls as well."""
import asyncio
import ipaddress
import re
import socket
from urllib.parse import urlsplit
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import secrets
from .config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def authenticate(key: str | None = Security(api_key_header)) -> None:
    if settings.api_key and not (key and secrets.compare_digest(key, settings.api_key)):
        raise HTTPException(status_code=401, detail="Valid X-API-Key required")
    # With no key, only bind to loopback. App startup sets this restriction.


def validate_url_syntax(url: str) -> tuple[str, str]:
    try:
        p = urlsplit(url)
        if p.scheme not in {"http", "https"} or not p.hostname or p.username or p.password:
            raise ValueError("Only HTTP(S) URLs without embedded credentials are permitted")
        host = p.hostname.lower().strip(".")
        if not host or len(url) > 4096 or re.search(r"[\x00-\x1f]", url):
            raise ValueError("Invalid URL")
        if not settings.allow_private_targets and p.port is not None and p.port not in {80, 443, 8080, 8000}:
            raise ValueError("Port not permitted")
        return url, host
    except (ValueError, TypeError) as exc:
        raise HTTPException(400, f"Unsafe or invalid URL: {exc}") from exc


async def validate_public_url(url: str, allowed_domains: list[str] | None = None) -> str:
    url, host = validate_url_syntax(url)
    if allowed_domains:
        allowed = [d.lower().strip(".") for d in allowed_domains]
        if not any(host == d or host.endswith("." + d) for d in allowed):
            raise HTTPException(403, "Host is not included in allowed_domains")
    if settings.allow_private_targets:
        return url
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise HTTPException(403, "Local targets are blocked")
    try:
        literal = ipaddress.ip_address(host)
        addresses = [literal]
    except ValueError:
        try:
            infos = await asyncio.wait_for(
                asyncio.get_running_loop().getaddrinfo(host, None, type=socket.SOCK_STREAM), 4.0
            )
            addresses = [ipaddress.ip_address(rec[4][0]) for rec in infos]
        except (OSError, TimeoutError, ValueError) as exc:
            raise HTTPException(400, f"Unable to resolve host: {exc}") from exc
    if not addresses or not all(ip.is_global for ip in addresses):
        raise HTTPException(403, "Private, loopback, reserved, and link-local destinations are blocked")
    return url
