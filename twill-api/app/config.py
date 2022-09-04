from typing import Optional

from pydantic import BaseSettings, Field

from app.service.starsessions.backends.redis import RedisBackend


class AppSettings(BaseSettings):
    environment: str = Field(env="environment", default="local")
    commit_hash: Optional[str] = Field(env="RENDER_GIT_COMMIT", default=None)


class RedisSettings(BaseSettings):
    redis_url: str


redis_settings = RedisSettings()
app_settings = AppSettings()


# authentication_settings = AuthenticationSettings()

session_backend = RedisBackend(
    redis_settings.redis_url,
    redis_key_func=lambda x: "session:" + x,
    expire=60 * 60 * 24 * 7,
)
