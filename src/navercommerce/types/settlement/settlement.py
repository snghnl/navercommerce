"""Settlement response types for the Naver Commerce SDK."""

from __future__ import annotations

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

    page: int | None = None
    size: int | None = None
    total_elements: int | None = Field(None, alias="totalElements")
    total_pages: int | None = Field(None, alias="totalPages")

    model_config = {"extra": "allow"}


class SettlementResponse(BaseModel):
    """
    Settlement query response.

    Contains settlement records and pagination info.
    """

    elements: list[SettlementElement] = Field(default_factory=list)
    pagination: Pagination | None = None

    model_config = {"extra": "allow"}
