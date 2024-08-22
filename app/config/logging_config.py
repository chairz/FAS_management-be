import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import os

# Define basic configuration
LOGGING_LEVEL = logging.DEBUG
LOGFILE_DIR = "logs"
LOGFILE_NAME = "fas_be.log"

# Create logs directory if it does not exist
if not os.path.exists(LOGFILE_DIR):
    os.makedirs(LOGFILE_DIR)

# Define loggers configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOGGING_LEVEL,
            "formatter": "default",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": LOGGING_LEVEL,
            "formatter": "default",
            "filename": os.path.join(LOGFILE_DIR, LOGFILE_NAME),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
        },
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": LOGGING_LEVEL,
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": LOGGING_LEVEL,
        },
        "myapp": {
            "handlers": ["console", "file"],
            "level": LOGGING_LEVEL,
        },
    },
}
