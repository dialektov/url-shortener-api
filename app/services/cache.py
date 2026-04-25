from redis import Redis

from app.core.config import settings

_client: Redis | None = None


def get_redis() -> Redis | None:
    global _client
    if _client is not None:
        return _client
    try:
        _client = Redis.from_url(settings.redis_url, decode_responses=True)
        _client.ping()
        return _client
    except Exception:
        _client = None
        return None
