import os
import sys
import uvicorn
from .config import settings

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    if host not in {"127.0.0.1", "::1", "localhost"} and not settings.api_key:
        sys.exit("Refusing public network bind without FALVORN_API_KEY")
    if host not in {"127.0.0.1", "::1", "localhost"} and settings.allow_private_targets:
        sys.exit("Refusing public network bind with ALLOW_PRIVATE_TARGETS=true")
    uvicorn.run("falvorn.api:app", host=host, port=int(os.getenv("PORT", "8000")))
