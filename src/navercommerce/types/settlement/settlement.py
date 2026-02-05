"""Settlement response types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ..._models import BaseModel


class SettlementElement(BaseModel):
    """
    Settlement element information.

    Represents a single settlement record with payment and commission details.
    """

    # Allow all fields as settlement structure varies by endpoint
    model_config = {"extra": "allow"}


class Pagination(BaseModel):
    """Pagination information for settlement queries."""

    page: Optional[int] = None
    size: Optional[int] = None
    total_elements: Optional[int] = Field(None, alias="totalElements")
    total_pages: Optional[int] = Field(None, alias="totalPages")

    model_config = {"extra": "allow"}


class SettlementResponse(BaseModel):
    """
    Settlement query response.

    Contains settlement records and pagination info.
    """

    elements: List[SettlementElement] = Field(default_factory=list)
    pagination: Optional[Pagination] = None

    model_config = {"extra": "allow"}
