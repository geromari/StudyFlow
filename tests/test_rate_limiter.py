"""Unit tests for rate limiter."""

import pytest

from app.utils.rate_limiter import InMemoryRateLimiter


@pytest.mark.asyncio
async def test_in_memory_rate_limiter() -> None:
    limiter = InMemoryRateLimiter()

    # Allow up to 3 requests in 10 seconds
    for _ in range(3):
        allowed = await limiter.is_allowed(key="user_123", limit=3, period_seconds=10)
        assert allowed is True

    # 4th request within period must be rejected
    rejected = await limiter.is_allowed(key="user_123", limit=3, period_seconds=10)
    assert rejected is False

    # Different key should still be allowed
    other_allowed = await limiter.is_allowed(key="user_456", limit=3, period_seconds=10)
    assert other_allowed is True

    # After reset, user_123 should be allowed again
    limiter.reset("user_123")
    assert await limiter.is_allowed(key="user_123", limit=3, period_seconds=10) is True
