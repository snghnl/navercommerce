"""Product brand types for the Naver Commerce SDK."""

from __future__ import annotations

from pydantic import Field

from ..._models import BaseModel


class Brand(BaseModel):
    """
    Product brand information.

    Represents a brand in the Naver Commerce system.
    """

    id: str
    name: str
    name_english: str | None = Field(None, alias="nameEnglish")


class BrandList(BaseModel):
    """List of brands."""

    brands: list[Brand]
    total_count: int = Field(alias="totalCount")
