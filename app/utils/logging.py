"""Logging configuration for StudyFlow."""

import logging
import re
import sys


class SensitiveDataFilter(logging.Filter):
    """Filter that sanitizes bot tokens, API keys, and sensitive authorization strings."""

    SENSITIVE_PATTERNS = [
        re.compile(r"(\d{8,10}:[A-Za-z0-9_-]{35})"),  # Telegram Bot Token
        re.compile(r"(sk-[A-Za-z0-9_-]{20,})"),       # OpenAI Key
        re.compile(r"(password=['\"][^'\"]*['\"])", re.IGNORECASE),
        re.compile(r"(api[_-]?key=['\"][^'\"]*['\"])", re.IGNORECASE),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            msg = record.msg
            for pattern in self.SENSITIVE_PATTERNS:
                msg = pattern.sub("[REDACTED]", msg)
            record.msg = msg
        return True


def setup_logging(log_level: str = "INFO") -> None:
    """Setup structured, filtered logging for the application."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(SensitiveDataFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Avoid duplicate handlers if called multiple times
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(handler)
    else:
        root_logger.handlers = [handler]

    # Silence overly verbose libraries
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
