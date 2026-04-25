from pydantic import BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = None
    ttl_seconds: int | None = None


class LinkOut(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    clicks: int

    model_config = ConfigDict(from_attributes=True)
