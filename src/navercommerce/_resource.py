"""Base resource classes for the Naver Commerce SDK."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

if TYPE_CHECKING:
    from ._client import AsyncNaverCommerce, NaverCommerce
    from ._types import Body, FileTypes, RequestOptions

ResponseT = TypeVar("ResponseT")


class SyncAPIResource:
    """
    Base class for synchronous API resources.

    Resource classes inherit from this to access the client's HTTP methods.
    This provides a clean separation between resource logic and HTTP implementation.
    """

    _client: NaverCommerce

    def __init__(self, client: NaverCommerce) -> None:
        self._client = client

    def _get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a GET request."""
        return self._client.get(path, cast_to=cast_to, options=options, **kwargs)

    def _post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Optional[Body] = None,
        files: Optional[dict[str, FileTypes]] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a POST request."""
        return self._client.post(
            path, cast_to=cast_to, body=body, files=files, options=options, **kwargs
        )

    def _put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Optional[Body] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PUT request."""
        return self._client.put(
            path, cast_to=cast_to, body=body, options=options, **kwargs
        )

    def _patch(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Optional[Body] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PATCH request."""
        return self._client.patch(
            path, cast_to=cast_to, body=body, options=options, **kwargs
        )

    def _delete(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a DELETE request."""
        return self._client.delete(path, cast_to=cast_to, options=options, **kwargs)

    def _sleep(self, seconds: float) -> None:
        """Sleep for the specified number of seconds."""
        time.sleep(seconds)


class AsyncAPIResource:
    """
    Base class for asynchronous API resources.

    Resource classes inherit from this to access the client's async HTTP methods.
    This provides a clean separation between resource logic and HTTP implementation.
    """

    _client: AsyncNaverCommerce

    def __init__(self, client: AsyncNaverCommerce) -> None:
        self._client = client

    async def _get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a GET request."""
        return await self._client.get(
            path, cast_to=cast_to, options=options, **kwargs
        )

    async def _post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Optional[Body] = None,
        files: Optional[dict[str, FileTypes]] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a POST request."""
        return await self._client.post(
            path, cast_to=cast_to, body=body, files=files, options=options, **kwargs
        )

    async def _put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Optional[Body] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PUT request."""
        return await self._client.put(
            path, cast_to=cast_to, body=body, options=options, **kwargs
        )

    async def _patch(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Optional[Body] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PATCH request."""
        return await self._client.patch(
            path, cast_to=cast_to, body=body, options=options, **kwargs
        )

    async def _delete(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a DELETE request."""
        return await self._client.delete(
            path, cast_to=cast_to, options=options, **kwargs
        )

    async def _sleep(self, seconds: float) -> None:
        """Sleep for the specified number of seconds."""
        import anyio

        await anyio.sleep(seconds)
