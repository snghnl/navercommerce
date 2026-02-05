"""Orders resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..._resource import AsyncAPIResource, SyncAPIResource

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class Orders(SyncAPIResource):
    """
    Orders resource for managing product orders.

    This resource provides access to:
    - Listing orders
    - Retrieving order details
    - Confirming orders
    - Managing shipping information
    """

    pass


class AsyncOrders(AsyncAPIResource):
    """
    Async orders resource for managing product orders.

    This resource provides async access to:
    - Listing orders
    - Retrieving order details
    - Confirming orders
    - Managing shipping information
    """

    pass
