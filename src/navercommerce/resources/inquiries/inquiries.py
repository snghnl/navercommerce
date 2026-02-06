"""Inquiries resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ..._resource import AsyncAPIResource, SyncAPIResource
from .notices import AsyncNotices, Notices
from .qnas import AsyncQnas, Qnas

if TYPE_CHECKING:
    pass


class Inquiries(SyncAPIResource):
    """
    Inquiries resource for managing customer interactions.

    This resource provides access to:
    - Product Q&As (questions and answers)
    - Seller notices
    """

    @cached_property
    def qnas(self) -> Qnas:
        """Access the Q&As sub-resource."""
        return Qnas(self._client)

    @cached_property
    def notices(self) -> Notices:
        """Access the Notices sub-resource."""
        return Notices(self._client)


class AsyncInquiries(AsyncAPIResource):
    """
    Async inquiries resource for managing customer interactions.

    This resource provides async access to:
    - Product Q&As (questions and answers)
    - Seller notices
    """

    @cached_property
    def qnas(self) -> AsyncQnas:
        """Access the async Q&As sub-resource."""
        return AsyncQnas(self._client)

    @cached_property
    def notices(self) -> AsyncNotices:
        """Access the async Notices sub-resource."""
        return AsyncNotices(self._client)
