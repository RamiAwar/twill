import logging
from typing import Optional, Tuple

import structlog
import uvicorn
from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    environment: str = Field(env="environment", default="local")
    commit_hash: Optional[str] = Field(env="RENDER_GIT_COMMIT", default=None)

    def is_local(self) -> bool:
        return self.environment == "local"


class RedisSettings(BaseSettings):
    redis_url: str


app_settings = AppSettings()
redis_settings = RedisSettings()

# TODO: Enable when need to scale
# from starsessions.stores.redis import RedisStore
# redis_store = RedisStore(redis_settings.redis_url, prefix="starsession:")


shared_processors: Tuple[structlog.types.Processor, ...] = (
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
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
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": shared_processors,
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": shared_processors,
        },
        **uvicorn.config.LOGGING_CONFIG["formatters"],
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json" if not app_settings.is_local() else "console",
        },
        "uvicorn.access": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "access",
        },
        "uvicorn.default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        # This will wrap any other loggers not defined here with JSON. If you're already logging json, use hideonfly logger to avoid this extra wrap
        "": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "hideonfly": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": [
                "default" if not app_settings.is_local() else "uvicorn.default"
            ],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": [
                "default" if not app_settings.is_local() else "uvicorn.access"
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    processors = [
        structlog.stdlib.filter_by_level,
        *shared_processors,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.config.dictConfig(logging_config)
