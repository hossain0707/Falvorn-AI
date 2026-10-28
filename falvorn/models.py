from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Any

class FetchRequest(BaseModel):
    url: str
    render_js: bool = False
    allowed_domains: list[str] | None = None

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    max_results: int = Field(10, ge=1, le=30)

class AgentRequest(BaseModel):
    url: str
    goal: str = Field(min_length=2, max_length=3000)
    allowed_domains: list[str] | None = None
    allow_write_actions: bool = False
    max_steps: int = Field(8, ge=1, le=30)

class BrowserRequest(BaseModel):
    url: str
    allowed_domains: list[str] | None = None

class BrowserAction(BaseModel):
    action: Literal["navigate", "click", "type", "scroll", "snapshot"]
    url: str | None = None
    index: int | None = Field(None, ge=0)
    text: str | None = None
    pixels: int = 600
    allow_write_actions: bool = False

class MonitorRequest(BaseModel):
    url: str
    key: str | None = None

class AgentDecision(BaseModel):
    action: Literal["click", "type", "scroll", "navigate", "done"]
    index: int | None = None
    url: str | None = None
    text: str | None = None
    answer: Any | None = None

class MonitorSubscriptionRequest(BaseModel):
    url: str
    interval_seconds: int = Field(3600, ge=300, le=604800)
