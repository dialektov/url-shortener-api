import secrets
import string
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Link
from app.schemas.link import LinkCreate
from app.services.cache import get_redis

ALPHABET = string.ascii_letters + string.digits


def generate_code(length: int = 7) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def create_short_link(db: Session, payload: LinkCreate) -> Link:
    code = payload.custom_alias or generate_code()
    if db.execute(select(Link).where(Link.short_code == code)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Alias already in use")

    expires_at = None
    if payload.ttl_seconds:
        expires_at = datetime.now(UTC) + timedelta(seconds=payload.ttl_seconds)

    link = Link(short_code=code, original_url=str(payload.original_url), expires_at=expires_at)
    db.add(link)
    db.commit()
    db.refresh(link)

    redis_client = get_redis()
    if redis_client:
        redis_client.setex(f"link:{link.short_code}", settings.cache_ttl_seconds, link.original_url)
    return link


def resolve_link(db: Session, code: str) -> Link:
    redis_client = get_redis()
    if redis_client:
        cached = redis_client.get(f"link:{code}")
        if cached:
            link = db.execute(select(Link).where(Link.short_code == code)).scalar_one_or_none()
            if not link:
                raise HTTPException(status_code=404, detail="Link not found")
            return link

    link = db.execute(select(Link).where(Link.short_code == code)).scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if link.expires_at and link.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=410, detail="Link expired")

    if redis_client:
        redis_client.setex(f"link:{code}", settings.cache_ttl_seconds, link.original_url)
    return link
