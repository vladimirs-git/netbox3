"""Wrappers for logging."""
import logging
import time


def set_logging_critical(func):
    """Set logging CRITICAL (disable logging) for function execution time."""

    def wrap(*args, **kwargs):
        """Wrap."""
        logger_o = logging.getLogger()
        level = logger_o.level
        logger_o.level = logging.CRITICAL

        _return = func(*args, **kwargs)

        logger_o.level = level
        return _return

    return wrap


def execution_time(func):
    """Log function execution time."""

    def wrapper(*args, **kwargs):
        """Wrap."""
        started = time.time()

        result = func(*args, **kwargs)

        elapsed = time.time() - started
        msg = f"Runtime: {func.__name__} {elapsed:.3f}s."
        logging.critical(msg)
        return result

    return wrapper
