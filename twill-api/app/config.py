from typing import Optional

from pydantic import BaseSettings, Field
from starsessions.stores.redis import RedisStore


class AppSettings(BaseSettings):
    environment: str = Field(env="environment", default="local")
    commit_hash: Optional[str] = Field(env="RENDER_GIT_COMMIT", default=None)


class RedisSettings(BaseSettings):
    redis_url: str


redis_settings = RedisSettings()
app_settings = AppSettings()


# authentication_settings = AuthenticationSettings()

redis_store = RedisStore(redis_settings.redis_url, prefix="starsession:")
