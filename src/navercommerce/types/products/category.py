"""Product category types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..._models import BaseModel


class Category(BaseModel):
    """
    Product category information.

    Represents a category in the Naver Commerce category hierarchy.
    """

    id: str
    name: str
    whole_category_name: Optional[str] = Field(None, alias="wholeCategoryName")
    last_level: Optional[bool] = Field(None, alias="lastLevel")
    parent_category_id: Optional[str] = Field(None, alias="parentCategoryId")


class CategoryList(BaseModel):
    """List of categories."""

    categories: list[Category]
    total_count: int = Field(alias="totalCount")
