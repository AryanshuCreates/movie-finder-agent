import time
from collections import defaultdict
from typing import List

# Time window (in seconds) during which we count requests
WINDOW_SECONDS = 10

# Max number of requests allowed per IP in that window
MAX_REQUESTS_PER_WINDOW = 10

# In-memory store: ip -> [timestamps]
_request_log: dict[str, List[float]] = defaultdict(list)


def is_allowed(ip: str) -> bool:
    """
    Very simple sliding-window rate limiter.

    - Keeps a list of timestamps for each IP.
    - On each request:
      - Drop timestamps older than WINDOW_SECONDS.
      - If there are still >= MAX_REQUESTS_PER_WINDOW timestamps, block.
      - Else, record this timestamp and allow.
    """
    now = time.time()
    window_start = now - WINDOW_SECONDS

    timestamps = _request_log[ip]

    # Keep only recent timestamps (inside window)
    recent = [t for t in timestamps if t >= window_start]
    _request_log[ip] = recent

    if len(recent) >= MAX_REQUESTS_PER_WINDOW:
        return False

    _request_log[ip].append(now)
    return True
