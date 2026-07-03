"""
logger.py — Application Logging Setup
=====================================
Configures structured console and file logging with standard formatting.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[str] = "INFO") -> logging.Logger:
    """Creates or retrieves a configured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger
