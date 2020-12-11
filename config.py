import os

LOG_LEVEL = os.getenv("LOG_LEVEL", default="DEBUG")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
            "datefmt": "%H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "console",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": True}
    },
}
