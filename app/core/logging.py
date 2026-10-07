import logging.config

from app.core.config import settings


def setup_logging() -> None:
    level = "DEBUG" if settings.DEBUG else "INFO"

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "default_value": "-",
                },
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s [%(correlation_id)s] [%(name)s] %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "filters": ["correlation_id"],
                },
            },
            "root": {"level": level, "handlers": ["console"]},
        }
    )
