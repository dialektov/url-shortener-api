from fastapi import FastAPI

from app.api.links import router as links_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(links_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
