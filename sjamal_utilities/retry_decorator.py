"""Retry decorator with exponential backoff.

Useful for transient failures (network requests, API calls, etc).
Logging is automatic via the standard logging module.
"""

import time
import logging
from functools import wraps
from typing import Callable, Optional, Tuple, Type


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """
    Decorator to retry a function with exponential backoff and optional jitter.

    Delay grows exponentially: delay * (backoff ^ attempt_number).
    Jitter adds randomness to prevent thundering herd.

    Args:
        max_attempts: Maximum number of attempts (default: 3).
        delay: Initial delay between retries in seconds (default: 1.0).
        backoff: Exponential backoff multiplier (default: 2.0).
        jitter: Add random jitter to delay (default: True).
        exceptions: Tuple of exception types to catch and retry on (default: (Exception,)).

    Returns:
        Decorated function that retries on failure.

    Example:
        @retry(max_attempts=3, delay=1, exceptions=(ValueError, TimeoutError))
        def flaky_function():
            # Retried up to 3 times on ValueError or TimeoutError
            pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(__name__)
            current_delay = delay

            # Attempt the function up to max_attempts times
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    # Final attempt failed - re-raise the exception
                    if attempt == max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise

                    # Calculate delay with optional jitter to prevent thundering herd
                    actual_delay = current_delay
                    if jitter:
                        import random

                        # Jitter: random value between 0.5 and 1.5 of current_delay
                        actual_delay = current_delay * (0.5 + random.random())

                    # Log the retry attempt and sleep
                    logger.warning(
                        f"Function {func.__name__} failed (attempt {attempt}/{max_attempts}), "
                        f"retrying in {actual_delay:.2f}s: {e}"
                    )
                    time.sleep(actual_delay)
                    # Exponential backoff for next attempt
                    current_delay *= backoff

        return wrapper

    return decorator
