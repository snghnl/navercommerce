"""Notice types for the Naver Commerce SDK."""

from __future__ import annotations

from pydantic import Field

from ..._models import BaseModel


class NoticeItem(BaseModel):
    """Seller notice item."""

    notice_id: str | None = Field(None, alias="noticeId")
    notice_type: str | None = Field(None, alias="noticeType")
    title: str | None = None
    content: str | None = None
    created_date: str | None = Field(None, alias="createdDate")
    modified_date: str | None = Field(None, alias="modifiedDate")

    model_config = {"extra": "allow"}


class NoticeResponse(BaseModel):
    """Response for notice queries."""

    contents: list[NoticeItem] = Field(default_factory=list)
    total_count: int | None = Field(None, alias="totalCount")

    model_config = {"extra": "allow"}
