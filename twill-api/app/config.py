from typing import Optional

import structlog
from pydantic import BaseSettings, Field

from app.service.starsessions.backends.redis import RedisBackend


class TwitterAPISettings(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str = Field(env="token_secret")
    callback_url: str = Field(
        env="twitter_callback_url", default="http://localhost:5173/auth/oauth"
    )


class AppSettings(BaseSettings):
    environment: str = Field(env="environment", default="local")
    commit_hash: Optional[str] = Field(env="RENDER_GIT_COMMIT", default=None)


class MongoSettings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = ""
    mongo_pass: str = ""
    mongo_db: str = "twill"

    @property
    def dsn(self):
        url = f"{self.mongo_host}:{self.mongo_port}/{self.mongo_db}"
        if self.mongo_user:
            return f"mongodb://{self.mongo_user}:{self.mongo_pass}@{url}"
        else:
            return f"mongodb://{url}"


class RedisSettings(BaseSettings):
    redis_url: str


twitter_api_settings = TwitterAPISettings()
mongo_settings = MongoSettings()
redis_settings = RedisSettings()
app_settings = AppSettings()


# authentication_settings = AuthenticationSettings()

session_backend = RedisBackend(
    redis_settings.redis_url,
    redis_key_func=lambda x: "session:" + x,
    expire=60 * 60 * 24 * 7,
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger("twill")
