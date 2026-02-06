"""Q&A types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ..._models import BaseModel


class QnaItem(BaseModel):
    """Q&A item information."""

    question_id: Optional[str] = Field(None, alias="questionId")
    product_id: Optional[str] = Field(None, alias="productId")
    product_name: Optional[str] = Field(None, alias="productName")
    question_content: Optional[str] = Field(None, alias="questionContent")
    answer_content: Optional[str] = Field(None, alias="answerContent")
    question_date: Optional[str] = Field(None, alias="questionDate")
    answer_date: Optional[str] = Field(None, alias="answerDate")

    model_config = {"extra": "allow"}


class QnaTemplate(BaseModel):
    """Q&A answer template."""

    template_id: Optional[str] = Field(None, alias="templateId")
    template_content: Optional[str] = Field(None, alias="templateContent")
    template_name: Optional[str] = Field(None, alias="templateName")

    model_config = {"extra": "allow"}


class QnaResponse(BaseModel):
    """Response for Q&A list queries."""

    contents: List[QnaItem] = Field(default_factory=list)
    total_count: Optional[int] = Field(None, alias="totalCount")
    last: Optional[bool] = None

    model_config = {"extra": "allow"}


class QnaTemplateResponse(BaseModel):
    """Response for Q&A template queries."""

    templates: List[QnaTemplate] = Field(default_factory=list)

    model_config = {"extra": "allow"}
