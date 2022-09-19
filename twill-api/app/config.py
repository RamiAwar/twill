from typing import Optional

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    environment: str = Field(env="environment", default="local")
    commit_hash: Optional[str] = Field(env="RENDER_GIT_COMMIT", default=None)


class RedisSettings(BaseSettings):
    redis_url: str


app_settings = AppSettings()


redis_settings = RedisSettings()

# TODO: Enable when need to scale
from starsessions.stores.redis import RedisStore

# redis_store = RedisStore(redis_settings.redis_url, prefix="starsession:")
