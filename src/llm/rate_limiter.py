"""
Simple rate limiter for LLM API requests.

Responsibilities
----------------
- Enforce a maximum request rate.
- Block until a request is allowed.
- Remain independent of any specific LLM provider.
"""

from __future__ import annotations

import time
from collections import deque


class RateLimiter:
    """
    Sliding-window rate limiter.

    The limiter blocks until issuing another request would
    remain within the configured requests-per-minute quota.
    """

    def __init__(
        self,
        requests_per_minute: int,
    ) -> None:
        """
        Initialize the rate limiter.

        Args:
            requests_per_minute:
                Maximum number of requests allowed within
                a rolling one-minute window.
        """

        self._requests_per_minute = requests_per_minute
        self._timestamps: deque[float] = deque()

    def acquire(
        self,
    ) -> None:
        """
        Wait until another request is permitted.
        """

        now = time.monotonic()

        while (
            self._timestamps
            and now - self._timestamps[0] >= 60.0
        ):
            self._timestamps.popleft()

        if len(self._timestamps) >= self._requests_per_minute:

            sleep_time = (
                60.0 - (now - self._timestamps[0])
            )

            if sleep_time > 0:

                time.sleep(sleep_time)

            now = time.monotonic()

            while (
                self._timestamps
                and now - self._timestamps[0] >= 60.0
            ):
                self._timestamps.popleft()

        self._timestamps.append(time.monotonic())


_SHARED_RATE_LIMITER: RateLimiter | None = None


def get_rate_limiter(
    requests_per_minute: int,
) -> RateLimiter:
    """
    Return the shared application-wide rate limiter.
    """

    global _SHARED_RATE_LIMITER

    if _SHARED_RATE_LIMITER is None:

        _SHARED_RATE_LIMITER = RateLimiter(
            requests_per_minute=requests_per_minute,
        )

    return _SHARED_RATE_LIMITER