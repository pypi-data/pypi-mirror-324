import functools
import logging
import sys
from typing import Any, Callable

from src.settings import DEBUG


def log_entry(func: Callable, logger: logging.Logger) -> Callable:
    """Decorator to log method entry with class and method names"""

    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        class_name = self.__class__.__name__
        method_name = func.__name__
        logger.debug(f"{class_name}.{method_name}() - Entering method")
        return func(self, *args, **kwargs)

    return wrapper


def setup_logger(name: str = "steev") -> tuple[logging.Logger, Callable]:
    """Set up and return a logger instance that logs to console"""
    logger = logging.getLogger(name)

    if not logger.handlers:  # Avoid adding handlers multiple times
        logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        # Create console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Add formatter to handler
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger, functools.partial(log_entry, logger=logger)
