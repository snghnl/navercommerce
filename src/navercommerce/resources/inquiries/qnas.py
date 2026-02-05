"""Q&As sub-resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given
from ...types.inquiries import QnaResponse, QnaTemplateResponse

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class Qnas(SyncAPIResource):
    """Q&As sub-resource for managing product questions and answers."""

    def list(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> QnaResponse:
        """
        List product Q&As with pagination.

        Args:
            page: Page number
            size: Page size
            **kwargs: Additional query parameters

        Returns:
            QnaResponse with Q&A list

        Example:
            ```python
            qnas = client.inquiries.qnas.list(page=0, size=20)
            for qna in qnas.contents:
                print(f"Q: {qna.question_content}")
                if qna.answer_content:
                    print(f"A: {qna.answer_content}")
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/contents/qnas",
            cast_to=QnaResponse,
            options={"params": params},
        )

    def answer(
        self,
        *,
        question_id: str,
        answer_content: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Answer a product question.

        Args:
            question_id: Question ID to answer
            answer_content: Answer content
            **kwargs: Additional parameters

        Returns:
            Answer response

        Example:
            ```python
            result = client.inquiries.qnas.answer(
                question_id="12345",
                answer_content="Thank you for your question. The answer is..."
            )
            ```
        """
        body: Dict[str, Any] = {
            "answerContent": answer_content,
        }
        body.update(kwargs)

        return self._put(
            f"/v1/contents/qnas/{question_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def list_templates(
        self,
        **kwargs: Any,
    ) -> QnaTemplateResponse:
        """
        Get saved answer templates.

        Args:
            **kwargs: Additional query parameters

        Returns:
            QnaTemplateResponse with template list

        Example:
            ```python
            templates = client.inquiries.qnas.list_templates()
            for template in templates.templates:
                print(f"Template: {template.template_name}")
            ```
        """
        return self._get(
            "/v1/contents/qnas/templates",
            cast_to=QnaTemplateResponse,
            options={"params": kwargs},
        )


class AsyncQnas(AsyncAPIResource):
    """Async Q&As sub-resource for managing product questions and answers."""

    async def list(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> QnaResponse:
        """List product Q&As with pagination."""
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/contents/qnas",
            cast_to=QnaResponse,
            options={"params": params},
        )

    async def answer(
        self,
        *,
        question_id: str,
        answer_content: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Answer a product question."""
        body: Dict[str, Any] = {
            "answerContent": answer_content,
        }
        body.update(kwargs)

        return await self._put(
            f"/v1/contents/qnas/{question_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def list_templates(
        self,
        **kwargs: Any,
    ) -> QnaTemplateResponse:
        """Get saved answer templates."""
        return await self._get(
            "/v1/contents/qnas/templates",
            cast_to=QnaTemplateResponse,
            options={"params": kwargs},
        )
