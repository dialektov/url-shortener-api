from collections import defaultdict, deque
from time import time

from fastapi import HTTPException

from app.core.config import settings

WINDOW = settings.rate_limit_window_seconds
MAX_REQUESTS = settings.rate_limit_max_requests
request_buckets: dict[str, deque[float]] = defaultdict(deque)


def check_rate_limit(client_key: str) -> None:
    now = time()
    bucket = request_buckets[client_key]
    while bucket and bucket[0] <= now - WINDOW:
        bucket.popleft()
    if len(bucket) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests")
    bucket.append(now)
