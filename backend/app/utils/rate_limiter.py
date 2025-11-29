"""
Simple in-memory rate limiter for development/testing.
Not suitable for multiple-process production use - use Redis for distributed systems.
"""
from time import time
from typing import Dict, List, Tuple

# stores timestamps of requests per key (IP address)
_request_log: Dict[str, List[float]] = {}

# Basic configuration
DEFAULT_LIMIT = 120  # requests
DEFAULT_WINDOW = 60  # seconds


def allow_request(key: str, limit: int = DEFAULT_LIMIT, window: int = DEFAULT_WINDOW) -> Tuple[bool, int]:
    """Check and record a request for key.

    Returns (allowed: bool, retry_after_seconds: int).
    """
    now = time()
    window_start = now - window

    history = _request_log.get(key, [])
    # Prune old entries
    history = [ts for ts in history if ts >= window_start]

    if len(history) >= limit:
        # calculate retry after
        retry_after = int(window - (now - history[0]))
        if retry_after < 0:
            retry_after = 1
        return False, retry_after

    # record request
    history.append(now)
    _request_log[key] = history

    return True, 0


def get_window_usage(key: str, window: int = DEFAULT_WINDOW) -> int:
    """Return number of requests in current window."""
    now = time()
    window_start = now - window
    history = _request_log.get(key, [])
    return len([ts for ts in history if ts >= window_start])
