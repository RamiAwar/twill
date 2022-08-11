import structlog
from pydantic import BaseSettings, Field

# TODO: Replace with library
from app.service.session import RedisBackend


class TwitterAPISettings(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str = Field(env="token_secret")


# class JWTAlgorithm(str, Enum):
#     HS256 = "HS256"
#     RS256 = "RS256"
#     ES256 = "ES256"


# class AuthenticationSettings(BaseSettings):
#     jwt_secret: str
#     jwt_algorithm: JWTAlgorithm = JWTAlgorithm.HS256
#     jwt_expiration_minutes: int = 30
#     jwt_refresh_expiration_delta: int = 86400


class PostgresSettings(BaseSettings):
    postgres_url: str


class RedisSettings(BaseSettings):
    redis_url: str


twitter_api_settings = TwitterAPISettings()
postgres_settings = PostgresSettings()
redis_settings = RedisSettings()

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
