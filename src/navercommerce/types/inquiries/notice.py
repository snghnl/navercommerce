"""Notice types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ..._models import BaseModel


class NoticeItem(BaseModel):
    """Seller notice item."""

    notice_id: Optional[str] = Field(None, alias="noticeId")
    notice_type: Optional[str] = Field(None, alias="noticeType")
    title: Optional[str] = None
    content: Optional[str] = None
    created_date: Optional[str] = Field(None, alias="createdDate")
    modified_date: Optional[str] = Field(None, alias="modifiedDate")

    model_config = {"extra": "allow"}


class NoticeResponse(BaseModel):
    """Response for notice queries."""

    contents: List[NoticeItem] = Field(default_factory=list)
    total_count: Optional[int] = Field(None, alias="totalCount")

    model_config = {"extra": "allow"}
