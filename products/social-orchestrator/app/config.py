"""Operator-controlled settings; never store third-party access tokens in SQLite."""
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    api_key: str
    db_path: str
    media_dir: str
    public_media_url: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    meta_token: str
    meta_ig_id: str
    meta_app_secret: str
    meta_verify_token: str
    linkedin_token: str
    linkedin_author: str
    linkedin_version: str
    youtube_token: str
    feed_query: str
    dry_run: bool

    @classmethod
    def from_env(cls):
        return cls(
            api_key=os.getenv('SOCIAL_API_KEY', ''),
            db_path=os.getenv('SOCIAL_DB_PATH', '/data/social.db'),
            media_dir=os.getenv('SOCIAL_MEDIA_DIR', '/data/media'),
            public_media_url=os.getenv('PUBLIC_MEDIA_URL', '').rstrip('/'),
            llm_api_key=os.getenv('LLM_API_KEY', ''),
            llm_base_url=os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1').rstrip('/'),
            llm_model=os.getenv('LLM_MODEL', 'gpt-4o-mini'),
            meta_token=os.getenv('META_ACCESS_TOKEN', ''),
            meta_ig_id=os.getenv('META_IG_USER_ID', ''),
            meta_app_secret=os.getenv('META_APP_SECRET', ''),
            meta_verify_token=os.getenv('META_VERIFY_TOKEN', ''),
            linkedin_token=os.getenv('LINKEDIN_ACCESS_TOKEN', ''),
            linkedin_author=os.getenv('LINKEDIN_AUTHOR_URN', ''),
            linkedin_version=os.getenv('LINKEDIN_VERSION', '202610'),
            youtube_token=os.getenv('YOUTUBE_ACCESS_TOKEN', ''),
            feed_query=os.getenv('NEWS_SEARCH_QUERY', 'artificial intelligence technology'),
            dry_run=os.getenv('SOCIAL_DRY_RUN', 'true').lower() != 'false',
        )

    def validate(self):
        if len(self.api_key) < 24 or self.api_key.startswith('CHANGE_ME'):
            raise RuntimeError('SOCIAL_API_KEY must be configured with at least 24 characters')
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.media_dir).mkdir(parents=True, exist_ok=True)
