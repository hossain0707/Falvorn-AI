"""Falvorn AI REST API. No TinyFish code or services are used."""
import asyncio
import hashlib
import json
import os
import sqlite3
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urljoin
import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from .security import authenticate, validate_public_url
from .config import settings
from .models import FetchRequest, SearchRequest, AgentRequest, BrowserRequest, BrowserAction, MonitorRequest, MonitorSubscriptionRequest
from .browser import pool, observe
from .agent import enqueue, get_run as lookup_run, list_runs as list_stored_runs, cancel as cancel_run, configure_store, shutdown_runs
from .extract import html_to_markdown

ROOT = Path(__file__).resolve().parent
DATA = Path(settings.data_dir).resolve()
run_store = None

async def monitor_scheduler():
    """Best-effort single-process scheduler; intentionally disabled during tests via setting."""
    while True:
        await asyncio.sleep(10)
        if run_store is None:
            continue
        for sub in run_store.subscriptions(due_only=True):
            try:
                result = await monitor(MonitorRequest(url=sub["url"], key="subscription:" + sub["id"]))
                run_store.mark_subscription(sub["id"], result["changed"])
            except Exception as exc:
                run_store.mark_subscription(sub["id"], None, str(exc)[:200])


@asynccontextmanager
async def lifespan(app):
    global run_store
    DATA.mkdir(parents=True, exist_ok=True)
    run_store = configure_store(str(DATA))
    with sqlite3.connect(DATA / "monitor.sqlite3") as db:
        db.execute("CREATE TABLE IF NOT EXISTS monitors (key TEXT PRIMARY KEY, hash TEXT NOT NULL, updated REAL NOT NULL)")
    scheduler = asyncio.create_task(monitor_scheduler()) if settings.monitor_scheduler_enabled else None
    try:
        yield
    finally:
        if scheduler:
            scheduler.cancel()
            await asyncio.gather(scheduler, return_exceptions=True)
        await shutdown_runs()
        await pool.shutdown()

app = FastAPI(title="Falvorn AI", version="0.2.0", lifespan=lifespan,
              description="Independent web search, fetch, browser control, monitoring, and goal-driven agent MVP")
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

@app.get("/", include_in_schema=False)
async def homepage():
    return FileResponse(ROOT / "static" / "index.html")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.2.0", "capabilities": {
        "fetch": True, "browser": True, "agent": True, "agent_llm_configured": bool(settings.llm_api_key),
        "search_configured": bool(settings.searxng_url), "monitor": True,
        "scheduled_monitoring": settings.monitor_scheduler_enabled, "durable_runs": run_store is not None},
        "active_browser_sessions": len(pool.sessions)}

@app.post("/v1/fetch", dependencies=[Depends(authenticate)])
async def fetch(req: FetchRequest):
    await validate_public_url(req.url, req.allowed_domains)
    if req.render_js:
        sid, session = await pool.open(req.url, req.allowed_domains)
        try:
            html = await session.page.content()
            output = html_to_markdown(html)
            return {"url": session.page.url, **output, "rendered": True}
        finally:
            await pool.close(sid)
    # Redirect targets must be validated explicitly. HTTPX does not auto-follow.
    url = req.url
    async with httpx.AsyncClient(timeout=18, follow_redirects=False,
                                  headers={"User-Agent": "FalvornAI/0.1 (+independent research tool)"}) as client:
        for _ in range(5):
            await validate_public_url(url, req.allowed_domains)
            async with client.stream("GET", url) as response:
                if response.status_code in {301, 302, 303, 307, 308}:
                    target = response.headers.get("location")
                    if not target:
                        raise HTTPException(502, "Redirect has no Location")
                    url = urljoin(url, target)
                    continue
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    raise HTTPException(502, f"Remote server responded {exc.response.status_code}") from exc
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type and "text/plain" not in content_type:
                    raise HTTPException(415, "Only HTML/text content is supported")
                parts, total = [], 0
                async for chunk in response.aiter_bytes():
                    total += len(chunk)
                    if total > settings.max_page_bytes:
                        raise HTTPException(413, "Page exceeds configured size limit")
                    parts.append(chunk)
                html = b"".join(parts).decode(response.encoding or "utf-8", errors="replace")
                return {"url": url, **html_to_markdown(html), "rendered": False}
        raise HTTPException(400, "Too many redirects")

@app.post("/v1/search", dependencies=[Depends(authenticate)])
async def search(req: SearchRequest):
    if not settings.searxng_url:
        raise HTTPException(503, "Configure SEARXNG_URL to enable independent search")
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(settings.searxng_url.rstrip("/") + "/search",
                                    params={"q": req.query, "format": "json"})
        response.raise_for_status()
        data = response.json()
    results = []
    for record in data.get("results", [])[:req.max_results]:
        url = record.get("url", "")
        try:
            await validate_public_url(url)
        except HTTPException:
            continue
        results.append({"title": record.get("title", ""), "url": url,
                        "snippet": record.get("content", "")[:700],
                        "engine": record.get("engine", "")})
    return {"query": req.query, "results": results}

@app.post("/v1/agent/runs", dependencies=[Depends(authenticate)], status_code=202)
async def start_agent(req: AgentRequest):
    await validate_public_url(req.url, req.allowed_domains)
    run = enqueue(req)
    return {"run_id": run.id, "status": run.status,
            "status_url": f"/v1/agent/runs/{run.id}",
            "events_url": f"/v1/agent/runs/{run.id}/events"}

@app.get("/v1/agent/runs", dependencies=[Depends(authenticate)])
async def get_runs(limit: int = 30):
    return {"runs": list_stored_runs(max(1, min(limit, 100)))}

@app.get("/v1/agent/runs/{run_id}", dependencies=[Depends(authenticate)])
async def get_run(run_id: str):
    result = lookup_run(run_id)
    if result is None:
        raise HTTPException(404, "Unknown run")
    return result

@app.post("/v1/agent/runs/{run_id}/cancel", dependencies=[Depends(authenticate)])
async def stop_run(run_id: str):
    return cancel_run(run_id)

@app.get("/v1/agent/runs/{run_id}/events", dependencies=[Depends(authenticate)])
async def events(run_id: str):
    if lookup_run(run_id) is None:
        raise HTTPException(404, "Unknown run")
    async def stream():
        seen = 0
        while True:
            run = lookup_run(run_id)
            if not run:break
            for item in run["events"][seen:]:
                yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"
            seen = len(run["events"])
            if run["status"] not in {"queued", "running"}:break
            await asyncio.sleep(.5)
    return StreamingResponse(stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.post("/v1/browser/sessions", dependencies=[Depends(authenticate)], status_code=201)
async def browser_create(req: BrowserRequest):
    sid, session = await pool.open(req.url, req.allowed_domains)
    return {"session_id": sid, "observation": await observe(session.page)}

@app.get("/v1/browser/sessions/{sid}", dependencies=[Depends(authenticate)])
async def browser_snapshot(sid: str):
    session = pool.get(sid)
    async with session.lock:
        return {"session_id": sid, "observation": await observe(session.page)}

@app.post("/v1/browser/sessions/{sid}/actions", dependencies=[Depends(authenticate)])
async def browser_action(sid: str, action: BrowserAction):
    session = pool.get(sid)
    async with session.lock:
        result = await session.action(action.action, action.index, action.text,
             action.url, action.pixels, action.allow_write_actions)
    return {"session_id": sid, "observation": result}

@app.get("/v1/browser/sessions/{sid}/screenshot", dependencies=[Depends(authenticate)])
async def browser_screenshot(sid: str):
    session = pool.get(sid)
    async with session.lock:
        content = await session.page.screenshot(type="png", full_page=False, animations="disabled")
    return Response(content=content, media_type="image/png", headers={"Cache-Control":"no-store"})

@app.delete("/v1/browser/sessions/{sid}", dependencies=[Depends(authenticate)])
async def browser_close(sid: str):
    pool.get(sid)
    await pool.close(sid)
    return {"closed": True}

@app.post("/v1/monitor/check", dependencies=[Depends(authenticate)])
async def monitor(req: MonitorRequest):
    result = await fetch(FetchRequest(url=req.url))
    key = req.key or req.url
    digest = hashlib.sha256(result["markdown"].encode()).hexdigest()
    with sqlite3.connect(DATA / "monitor.sqlite3") as db:
        previous = db.execute("SELECT hash FROM monitors WHERE key=?", (key,)).fetchone()
        db.execute("INSERT INTO monitors(key,hash,updated) VALUES(?,?,?) "
                   "ON CONFLICT(key) DO UPDATE SET hash=excluded.hash,updated=excluded.updated",
                   (key, digest, time.time()))
    return {"key": key, "url": result["url"], "changed": previous is not None and previous[0] != digest,
            "first_check": previous is None, "content_hash": digest,
            "previous_hash": previous[0] if previous else None,
            "title": result["title"]}


@app.post("/v1/monitor/subscriptions", dependencies=[Depends(authenticate)], status_code=201)
async def subscribe_monitor(req: MonitorSubscriptionRequest):
    await validate_public_url(req.url)
    if run_store is None:
        raise HTTPException(503, "Storage unavailable")
    if len(run_store.subscriptions()) >= 100:
        raise HTTPException(429, "Subscription limit reached")
    return run_store.add_subscription(uuid.uuid4().hex, req.url, req.interval_seconds)

@app.get("/v1/monitor/subscriptions", dependencies=[Depends(authenticate)])
async def subscribed_monitors():
    return {"subscriptions": run_store.subscriptions() if run_store else []}

@app.post("/v1/monitor/subscriptions/{subscription_id}/pause", dependencies=[Depends(authenticate)])
async def pause_subscription(subscription_id: str):
    result = run_store.update_subscription(subscription_id, False) if run_store else None
    if result is None:raise HTTPException(404, "Unknown subscription")
    return result

@app.post("/v1/monitor/subscriptions/{subscription_id}/resume", dependencies=[Depends(authenticate)])
async def resume_subscription(subscription_id: str):
    result = run_store.update_subscription(subscription_id, True) if run_store else None
    if result is None:raise HTTPException(404, "Unknown subscription")
    return result

@app.delete("/v1/monitor/subscriptions/{subscription_id}", dependencies=[Depends(authenticate)])
async def delete_subscription(subscription_id: str):
    if not run_store or not run_store.delete_subscription(subscription_id):
        raise HTTPException(404, "Unknown subscription")
    return {"deleted": True}
