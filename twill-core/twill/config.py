import structlog
from pydantic import BaseSettings, Field


class TwitterAPISettings(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str = Field(env="token_secret")
    callback_url: str = Field(env="twitter_callback_url", default="http://localhost:5173/auth/oauth")


class MongoSettings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = ""
    mongo_pass: str = ""
    mongo_db: str = "twill"
    mongo_dsn: str = ""

    @property
    def dsn(self):
        if self.mongo_dsn:
            return self.mongo_dsn

        url = f"{self.mongo_host}:{self.mongo_port}/{self.mongo_db}"
        if self.mongo_user:
            return f"mongodb://{self.mongo_user}:{self.mongo_pass}@{url}"
        else:
            return f"mongodb://{url}"


mongo_settings = MongoSettings()
twitter_api_settings = TwitterAPISettings()


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
