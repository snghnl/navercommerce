"""Q&A types for the Naver Commerce SDK."""

from __future__ import annotations

from pydantic import Field

from ..._models import BaseModel


class QnaItem(BaseModel):
    """Q&A item information."""

    question_id: str | None = Field(None, alias="questionId")
    product_id: str | None = Field(None, alias="productId")
    product_name: str | None = Field(None, alias="productName")
    question_content: str | None = Field(None, alias="questionContent")
    answer_content: str | None = Field(None, alias="answerContent")
    question_date: str | None = Field(None, alias="questionDate")
    answer_date: str | None = Field(None, alias="answerDate")

    model_config = {"extra": "allow"}


class QnaTemplate(BaseModel):
    """Q&A answer template."""

    template_id: str | None = Field(None, alias="templateId")
    template_content: str | None = Field(None, alias="templateContent")
    template_name: str | None = Field(None, alias="templateName")

    model_config = {"extra": "allow"}


class QnaResponse(BaseModel):
    """Response for Q&A list queries."""

    contents: list[QnaItem] = Field(default_factory=list)
    total_count: int | None = Field(None, alias="totalCount")
    last: bool | None = None

    model_config = {"extra": "allow"}


class QnaTemplateResponse(BaseModel):
    """Response for Q&A template queries."""

    templates: list[QnaTemplate] = Field(default_factory=list)

    model_config = {"extra": "allow"}
