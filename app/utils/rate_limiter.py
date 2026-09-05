"""Rate limiting utilities using in-memory window or Redis."""

import time
from collections import defaultdict
from typing import Any, Protocol


class RateLimiterProtocol(Protocol):
    async def is_allowed(self, key: str, limit: int, period_seconds: int) -> bool: ...


class InMemoryRateLimiter:
    """Sliding-window rate limiter stored in memory."""

    def __init__(self) -> None:
        self._history: dict[str, list[float]] = defaultdict(list)

    async def is_allowed(self, key: str, limit: int, period_seconds: int) -> bool:
        now = time.time()
        cutoff = now - period_seconds

        # Clean old timestamps
        timestamps = [t for t in self._history[key] if t > cutoff]
        if len(timestamps) >= limit:
            self._history[key] = timestamps
            return False

        timestamps.append(now)
        self._history[key] = timestamps
        return True

    def reset(self, key: str | None = None) -> None:
        if key:
            self._history.pop(key, None)
        else:
            self._history.clear()


class RedisRateLimiter:
    """Sliding-window rate limiter using Redis sorted sets."""

    def __init__(self, redis_client: Any) -> None:
        self.redis = redis_client

    async def is_allowed(self, key: str, limit: int, period_seconds: int) -> bool:
        now = time.time()
        cutoff = now - period_seconds
        redis_key = f"studyflow:ratelimit:{key}"

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(redis_key, 0, cutoff)
        pipe.zcard(redis_key)
        pipe.zadd(redis_key, {str(now): now})
        pipe.expire(redis_key, period_seconds + 1)
        results = await pipe.execute()

        current_count = results[1]
        return current_count < limit


# Default global memory limiter (can be swapped or complemented by Redis)
default_limiter = InMemoryRateLimiter()
