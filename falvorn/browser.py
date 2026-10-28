"""Isolated Playwright sessions with URL checks and bounded observations."""
import asyncio
import re
import time
import uuid
from fastapi import HTTPException
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from .security import validate_public_url
from .config import settings

DANGEROUS = re.compile(r"\b(pay|purchase|place order|confirm order|send|submit|delete|remove account|transfer|checkout|buy now|publish|post|apply now|book now|withdraw)\b", re.I)
SENSITIVE = re.compile(r"(password|passcode|credit.?card|cvv|ssn|otp|one.?time|secret|token)", re.I)
SELECTOR = "a, button, input, textarea, select, [role='button'], [role='link']"

async def observe(page: Page) -> dict:
    # Input values are deliberately not returned, to reduce secret exposure.
    items = await page.locator(SELECTOR).evaluate_all("""els => els.slice(0,120).map((el,i) => ({
        index:i, tag:el.tagName.toLowerCase(), type:(el.getAttribute('type')||'').slice(0,40),
        label:(el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.innerText || el.getAttribute('name') || '').trim().replace(/\\s+/g,' ').slice(0,100),
        href:el.tagName === 'A' ? el.getAttribute('href') : undefined
    }))""")
    text = await page.locator("body").inner_text(timeout=7000)
    return {"url": page.url, "title": await page.title(), "text": text[:9000], "elements": items}

class Session:
    def __init__(self, context: BrowserContext, page: Page, allowed_domains: list[str] | None = None):
        self.context = context
        self.page = page
        self.allowed_domains = allowed_domains
        self.created = time.time()
        self.lock = asyncio.Lock()

    async def close(self):
        await self.context.close()

    async def route(self, route):
        # Validate every navigation and subresource egress attempt; DNS may change after validation,
        # so production networks must ALSO enforce egress at proxy/firewall level.
        try:
            await validate_public_url(route.request.url, self.allowed_domains)
            await route.continue_()
        except Exception:
            await route.abort()

    async def goto(self, url: str):
        await validate_public_url(url, self.allowed_domains)
        try:
            await self.page.goto(url, wait_until="domcontentloaded", timeout=25000)
        except Exception as exc:
            raise HTTPException(502, f"Browser navigation failed: {str(exc)[:220]}") from exc
        return await observe(self.page)

    async def action(self, action: str, index: int | None = None, text: str | None = None,
                     url: str | None = None, pixels: int = 600, allow_write_actions: bool = False):
        if action == "navigate":
            if not url:
                raise HTTPException(400, "Navigate requires URL")
            return await self.goto(url)
        if action == "scroll":
            await self.page.mouse.wheel(0, max(-2000, min(2000, pixels)))
        elif action in {"click", "type"}:
            if index is None:
                raise HTTPException(400, "Element index required")
            elements = self.page.locator(SELECTOR)
            if index >= min(await elements.count(), 120):
                raise HTTPException(400, "Element index no longer exists")
            el = elements.nth(index)
            meta = await el.evaluate("el => ({tag:el.tagName.toLowerCase(),type:el.type||'', label:(el.innerText||el.getAttribute('aria-label')||el.getAttribute('value')||'').slice(0,150)})")
            if action == "type":
                if meta["tag"] not in {"input", "textarea"}:
                    raise HTTPException(403, "Typing is restricted to text fields")
                if SENSITIVE.search(meta["type"] + ' ' + meta["label"]):
                    raise HTTPException(403, "Sensitive fields require a dedicated credential workflow")
                if not allow_write_actions:
                    raise HTTPException(403, "Typing requires allow_write_actions=true")
                await el.fill((text or "")[:1000], timeout=7000)
            else:
                if meta["tag"] not in {"a"} and not allow_write_actions:
                    raise HTTPException(403, "Button interaction requires allow_write_actions=true")
                if DANGEROUS.search(meta["label"]):
                    raise HTTPException(403, "Consequential action blocked; perform it manually")
                await el.click(timeout=8000)
        elif action != "snapshot":
            raise HTTPException(400, "Unsupported action")
        await self.page.wait_for_timeout(350)
        return await observe(self.page)

class BrowserPool:
    def __init__(self):
        self.browser: Browser | None = None
        self.playwright = None
        self.sessions: dict[str, Session] = {}
        self.lock = asyncio.Lock()

    async def start(self):
        if self.browser:
            return
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=settings.headless,
            executable_path="/usr/bin/chromium" if __import__('os').path.exists('/usr/bin/chromium') else None,
            args=["--no-sandbox", "--disable-dev-shm-usage"])

    async def open(self, url: str, allowed_domains: list[str] | None = None) -> tuple[str, Session]:
        async with self.lock:
            if len(self.sessions) >= settings.max_active_browsers:
                raise HTTPException(429, "Concurrent browser session limit reached")
            await validate_public_url(url, allowed_domains)
            await self.start()
            context = await self.browser.new_context(accept_downloads=False, service_workers="block")
            page = await context.new_page()
            session = Session(context, page, allowed_domains)
            await context.route("**/*", session.route)
            try:
                await session.goto(url)
            except Exception:
                await session.close()
                raise
            id_ = uuid.uuid4().hex
            self.sessions[id_] = session
            return id_, session

    def get(self, sid: str) -> Session:
        if sid not in self.sessions:
            raise HTTPException(404, "Session not found")
        return self.sessions[sid]

    async def close(self, sid: str):
        session = self.sessions.pop(sid, None)
        if session:
            await session.close()

    async def shutdown(self):
        for sid in list(self.sessions):
            await self.close(sid)
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

pool = BrowserPool()
