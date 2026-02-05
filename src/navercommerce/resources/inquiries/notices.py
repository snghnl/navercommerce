"""Notices sub-resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given
from ...types.inquiries import NoticeResponse, NoticeItem

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class Notices(SyncAPIResource):
    """Notices sub-resource for managing seller notices."""

    def create(
        self,
        *,
        notice_type: str,
        title: str,
        content: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a seller notice.

        Args:
            notice_type: Notice type (e.g., "EVENT", "NOTICE")
            title: Notice title
            content: Notice content
            **kwargs: Additional parameters

        Returns:
            Creation response

        Example:
            ```python
            result = client.inquiries.notices.create(
                notice_type="EVENT",
                title="New Product Launch",
                content="We are excited to announce..."
            )
            ```
        """
        body: Dict[str, Any] = {
            "noticeType": notice_type,
            "title": title,
            "content": content,
        }
        body.update(kwargs)

        return self._post(
            "/v1/contents/seller-notices",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def list(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> NoticeResponse:
        """
        List seller notices with pagination.

        Args:
            page: Page number
            size: Page size
            **kwargs: Additional query parameters

        Returns:
            NoticeResponse with notice list

        Example:
            ```python
            notices = client.inquiries.notices.list(page=0, size=20)
            for notice in notices.contents:
                print(f"Notice: {notice.title}")
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/contents/seller-notices",
            cast_to=NoticeResponse,
            options={"params": params},
        )

    def retrieve(
        self,
        notice_id: str,
        **kwargs: Any,
    ) -> NoticeItem:
        """
        Get a single notice.

        Args:
            notice_id: Notice ID
            **kwargs: Additional query parameters

        Returns:
            NoticeItem with notice details

        Example:
            ```python
            notice = client.inquiries.notices.retrieve("12345")
            print(f"Title: {notice.title}")
            print(f"Content: {notice.content}")
            ```
        """
        return self._get(
            f"/v1/contents/seller-notices/{notice_id}",
            cast_to=NoticeItem,
            options={"params": kwargs},
        )

    def update(
        self,
        *,
        notice_id: str,
        notice_type: str | NotGiven = not_given,
        title: str | NotGiven = not_given,
        content: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update a seller notice.

        Args:
            notice_id: Notice ID to update
            notice_type: Notice type
            title: Notice title
            content: Notice content
            **kwargs: Additional parameters

        Returns:
            Update response

        Example:
            ```python
            result = client.inquiries.notices.update(
                notice_id="12345",
                title="Updated Title",
                content="Updated content..."
            )
            ```
        """
        body: Dict[str, Any] = {}

        if not isinstance(notice_type, NotGiven):
            body["noticeType"] = notice_type
        if not isinstance(title, NotGiven):
            body["title"] = title
        if not isinstance(content, NotGiven):
            body["content"] = content

        body.update(kwargs)

        return self._put(
            f"/v1/contents/seller-notices/{notice_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def delete(
        self,
        notice_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Delete a seller notice.

        Args:
            notice_id: Notice ID to delete
            **kwargs: Additional parameters

        Returns:
            Deletion response

        Example:
            ```python
            result = client.inquiries.notices.delete("12345")
            ```
        """
        return self._delete(
            f"/v1/contents/seller-notices/{notice_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )


class AsyncNotices(AsyncAPIResource):
    """Async notices sub-resource for managing seller notices."""

    async def create(
        self,
        *,
        notice_type: str,
        title: str,
        content: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Create a seller notice."""
        body: Dict[str, Any] = {
            "noticeType": notice_type,
            "title": title,
            "content": content,
        }
        body.update(kwargs)

        return await self._post(
            "/v1/contents/seller-notices",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def list(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> NoticeResponse:
        """List seller notices with pagination."""
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/contents/seller-notices",
            cast_to=NoticeResponse,
            options={"params": params},
        )

    async def retrieve(
        self,
        notice_id: str,
        **kwargs: Any,
    ) -> NoticeItem:
        """Get a single notice."""
        return await self._get(
            f"/v1/contents/seller-notices/{notice_id}",
            cast_to=NoticeItem,
            options={"params": kwargs},
        )

    async def update(
        self,
        *,
        notice_id: str,
        notice_type: str | NotGiven = not_given,
        title: str | NotGiven = not_given,
        content: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Update a seller notice."""
        body: Dict[str, Any] = {}

        if not isinstance(notice_type, NotGiven):
            body["noticeType"] = notice_type
        if not isinstance(title, NotGiven):
            body["title"] = title
        if not isinstance(content, NotGiven):
            body["content"] = content

        body.update(kwargs)

        return await self._put(
            f"/v1/contents/seller-notices/{notice_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def delete(
        self,
        notice_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Delete a seller notice."""
        return await self._delete(
            f"/v1/contents/seller-notices/{notice_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )
