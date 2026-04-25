from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import Link
from app.schemas.link import LinkCreate, LinkOut
from app.services.rate_limit import check_rate_limit
from app.services.shortener import create_short_link, resolve_link

router = APIRouter(tags=["links"])


@router.post("/links", response_model=LinkOut, status_code=201)
def shorten_link(payload: LinkCreate, request: Request, db: Session = Depends(get_db)) -> LinkOut:
    check_rate_limit(request.client.host if request.client else "unknown")
    link = create_short_link(db, payload)
    return LinkOut(
        short_code=link.short_code,
        short_url=f"{settings.base_url}/{link.short_code}",
        original_url=link.original_url,
        clicks=link.clicks,
    )


@router.get("/{code}")
def redirect(code: str, request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    check_rate_limit(request.client.host if request.client else "unknown")
    link = resolve_link(db, code)
    link.clicks += 1
    db.add(link)
    db.commit()
    return RedirectResponse(url=link.original_url, status_code=307)


@router.get("/links/{code}/stats", response_model=LinkOut)
def link_stats(code: str, request: Request, db: Session = Depends(get_db)) -> LinkOut:
    check_rate_limit(request.client.host if request.client else "unknown")
    link = db.execute(select(Link).where(Link.short_code == code)).scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return LinkOut(
        short_code=link.short_code,
        short_url=f"{settings.base_url}/{link.short_code}",
        original_url=link.original_url,
        clicks=link.clicks,
    )
