"""
Rate limiting for claims processing
Implements token bucket algorithm for fair request distribution
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Tuple
from src.logger import setup_logger

logger = setup_logger(__name__)


class RateLimiter:
    """Token bucket rate limiter for requests"""

    def __init__(self, requests_per_minute: int = 20):
        """
        Initialize rate limiter

        Args:
            requests_per_minute: Max requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_second = requests_per_minute / 60.0
        self.tokens = float(requests_per_minute)
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, tokens: float = 1.0) -> bool:
        """
        Try to acquire tokens immediately.

        Args:
            tokens: Number of tokens to acquire (default 1.0)

        Returns:
            True if tokens available, False if rate limited
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(
                float(self.requests_per_minute),
                self.tokens + elapsed * self.requests_per_second
            )
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                logger.info(f"Rate limit: acquired {tokens} tokens. Remaining: {self.tokens:.2f}")
                return True

            logger.warning(f"Rate limit: not enough tokens. Need: {tokens}, Have: {self.tokens:.2f}")
            return False

    def wait_if_needed(self, tokens: float = 1.0) -> float:
        """
        Wait until tokens are available.

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds (0 if no wait needed)
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update

            self.tokens = min(
                float(self.requests_per_minute),
                self.tokens + elapsed * self.requests_per_second
            )
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0

            # Calculate wait time
            wait_time = (tokens - self.tokens) / self.requests_per_second
            self.tokens = 0

            logger.info(f"Rate limit: waiting {wait_time:.2f}s for {tokens} tokens")
            return wait_time

    def get_status(self) -> dict:
        """Get current rate limiter status"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            tokens = min(
                float(self.requests_per_minute),
                self.tokens + elapsed * self.requests_per_second
            )
            return {
                "tokens_available": tokens,
                "tokens_max": self.requests_per_minute,
                "requests_per_minute": self.requests_per_minute,
                "requests_per_second": self.requests_per_second
            }


class UserRateLimiter:
    """Per-user rate limiting"""

    def __init__(self, requests_per_hour: int = 100):
        """
        Initialize user rate limiter

        Args:
            requests_per_hour: Max requests per user per hour
        """
        self.requests_per_hour = requests_per_hour
        self.user_requests = defaultdict(list)
        self.lock = Lock()

    def check_limit(self, user_id: str) -> Tuple[bool, int]:
        """
        Check if user exceeded limit.

        Args:
            user_id: User identifier

        Returns:
            Tuple of (allowed: bool, requests_remaining: int)
        """
        with self.lock:
            now = time.time()
            one_hour_ago = now - 3600

            # Remove old requests outside the hour window
            requests = [
                t for t in self.user_requests[user_id]
                if t > one_hour_ago
            ]
            self.user_requests[user_id] = requests

            # Check limit
            if len(requests) >= self.requests_per_hour:
                logger.warning(f"User {user_id} exceeded rate limit: {len(requests)}/{self.requests_per_hour}")
                return False, 0

            # Add current request
            requests.append(now)
            remaining = self.requests_per_hour - len(requests)

            logger.info(f"User {user_id}: {len(requests)}/{self.requests_per_hour} requests. Remaining: {remaining}")

            return True, remaining

    def get_user_stats(self, user_id: str) -> dict:
        """Get user statistics"""
        with self.lock:
            now = time.time()
            one_hour_ago = now - 3600

            requests = [
                t for t in self.user_requests[user_id]
                if t > one_hour_ago
            ]

            return {
                "user_id": user_id,
                "requests_this_hour": len(requests),
                "requests_limit": self.requests_per_hour,
                "requests_remaining": max(0, self.requests_per_hour - len(requests))
            }


# Global instances
claim_limiter = RateLimiter(requests_per_minute=20)
user_limiter = UserRateLimiter(requests_per_hour=100)
