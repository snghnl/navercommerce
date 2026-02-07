"""Product category types for the Naver Commerce SDK."""

from __future__ import annotations

from pydantic import Field

from ..._models import BaseModel


class Category(BaseModel):
    """
    Product category information.

    Represents a category in the Naver Commerce category hierarchy.
    """

    id: str
    name: str
    whole_category_name: str | None = Field(None, alias="wholeCategoryName")
    last_level: bool | None = Field(None, alias="lastLevel")
    parent_category_id: str | None = Field(None, alias="parentCategoryId")


class CategoryList(BaseModel):
    """List of categories."""

    categories: list[Category]
    total_count: int = Field(alias="totalCount")
