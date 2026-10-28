from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"true", "1", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("FALVORN_API_KEY", "")
    llm_api_url: str = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4.1-mini")
    searxng_url: str = os.getenv("SEARXNG_URL", "")
    allow_private_targets: bool = flag("ALLOW_PRIVATE_TARGETS")
    max_agent_steps: int = max(1, min(30, int(os.getenv("MAX_AGENT_STEPS", "12"))))
    max_active_browsers: int = max(1, min(10, int(os.getenv("MAX_ACTIVE_BROWSERS", "3"))))
    max_page_bytes: int = max(1024, min(4_000_000, int(os.getenv("MAX_PAGE_BYTES", "1000000"))))
    headless: bool = flag("BROWSER_HEADLESS", True)
    data_dir: str = os.getenv("DATA_DIR", "./data")
    monitor_scheduler_enabled: bool = flag("MONITOR_SCHEDULER_ENABLED", False)

settings = Settings()
