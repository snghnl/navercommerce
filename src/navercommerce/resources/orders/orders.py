"""Orders resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given
from ...types.orders import Order, OrderProductInfo

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class Orders(SyncAPIResource):
    """
    Orders resource for managing product orders.

    This resource provides access to:
    - Listing orders by date range
    - Retrieving order details
    - Confirming orders
    - Managing shipping information
    """

    def list(
        self,
        *,
        start_date: str,
        end_date: str,
        last_changed_from: str | NotGiven = not_given,
        last_changed_to: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[OrderProductInfo]:
        """
        List orders within a date range.

        Args:
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            last_changed_from: Filter by last changed date from (YYYY-MM-DD)
            last_changed_to: Filter by last changed date to (YYYY-MM-DD)
            **kwargs: Additional query parameters

        Returns:
            List of OrderProductInfo objects

        Example:
            ```python
            orders = client.orders.list(
                start_date="2024-01-01",
                end_date="2024-01-31"
            )
            for order in orders:
                print(f"Order: {order.product_order_id}")
                print(f"Product: {order.product_name}")
                print(f"Status: {order.order_status}")
            ```
        """
        body: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(last_changed_from, NotGiven):
            body["lastChangedFrom"] = last_changed_from
        if not isinstance(last_changed_to, NotGiven):
            body["lastChangedTo"] = last_changed_to

        body.update(kwargs)

        return self._post(
            "/v1/orders/product-orders/list-query",
            cast_to=List[OrderProductInfo],  # type: ignore
            body=body,
        )

    def retrieve(self, product_order_id: str) -> Order:
        """
        Retrieve detailed information for a specific order.

        Args:
            product_order_id: Product order ID

        Returns:
            Order object with full details

        Example:
            ```python
            order = client.orders.retrieve("2024010112345678")
            print(f"Order ID: {order.order_id}")
            print(f"Order Date: {order.order_date}")
            print(f"Total: {order.total_payment_amount}원")
            ```
        """
        return self._get(
            f"/v1/orders/product-orders/{product_order_id}",
            cast_to=Order,
        )

    def confirm(
        self,
        *,
        product_order_ids: List[str],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Confirm order acceptance.

        This must be called after payment is confirmed and before shipping.

        Args:
            product_order_ids: List of product order IDs to confirm
            **kwargs: Additional parameters

        Returns:
            Confirmation response

        Example:
            ```python
            result = client.orders.confirm(
                product_order_ids=["2024010112345678", "2024010112345679"]
            )
            print(f"Confirmed {len(result)} orders")
            ```
        """
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
        }
        body.update(kwargs)

        return self._post(
            "/v1/orders/confirm",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def ship(
        self,
        *,
        product_order_ids: List[str],
        shipping_company: str,
        tracking_number: str,
        shipping_date: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Register shipping information for orders.

        Args:
            product_order_ids: List of product order IDs to ship
            shipping_company: Shipping company name (e.g., "CJ대한통운", "우체국택배")
            tracking_number: Tracking/invoice number
            shipping_date: Shipping date (YYYY-MM-DD format)
            **kwargs: Additional parameters

        Returns:
            Shipping registration response

        Example:
            ```python
            result = client.orders.ship(
                product_order_ids=["2024010112345678"],
                shipping_company="CJ대한통운",
                tracking_number="123456789012",
                shipping_date="2024-01-15"
            )
            print("Shipping registered")
            ```
        """
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
            "deliveryCompany": shipping_company,
            "trackingNumber": tracking_number,
        }

        if not isinstance(shipping_date, NotGiven):
            body["shippingDate"] = shipping_date

        body.update(kwargs)

        return self._post(
            "/v1/orders/ship",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def cancel(
        self,
        *,
        product_order_ids: List[str],
        cancel_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Cancel orders.

        Args:
            product_order_ids: List of product order IDs to cancel
            cancel_reason: Reason for cancellation
            **kwargs: Additional parameters

        Returns:
            Cancellation response

        Example:
            ```python
            result = client.orders.cancel(
                product_order_ids=["2024010112345678"],
                cancel_reason="Out of stock"
            )
            ```
        """
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
            "cancelReason": cancel_reason,
        }
        body.update(kwargs)

        return self._post(
            "/v1/orders/cancel",
            cast_to=dict,  # type: ignore
            body=body,
        )


class AsyncOrders(AsyncAPIResource):
    """
    Async orders resource for managing product orders.

    This resource provides async access to:
    - Listing orders by date range
    - Retrieving order details
    - Confirming orders
    - Managing shipping information
    """

    async def list(
        self,
        *,
        start_date: str,
        end_date: str,
        last_changed_from: str | NotGiven = not_given,
        last_changed_to: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[OrderProductInfo]:
        """
        List orders within a date range.

        Args:
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            last_changed_from: Filter by last changed date from (YYYY-MM-DD)
            last_changed_to: Filter by last changed date to (YYYY-MM-DD)
            **kwargs: Additional query parameters

        Returns:
            List of OrderProductInfo objects
        """
        body: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }

        if not isinstance(last_changed_from, NotGiven):
            body["lastChangedFrom"] = last_changed_from
        if not isinstance(last_changed_to, NotGiven):
            body["lastChangedTo"] = last_changed_to

        body.update(kwargs)

        return await self._post(
            "/v1/orders/product-orders/list-query",
            cast_to=List[OrderProductInfo],  # type: ignore
            body=body,
        )

    async def retrieve(self, product_order_id: str) -> Order:
        """
        Retrieve detailed information for a specific order.

        Args:
            product_order_id: Product order ID

        Returns:
            Order object with full details
        """
        return await self._get(
            f"/v1/orders/product-orders/{product_order_id}",
            cast_to=Order,
        )

    async def confirm(
        self,
        *,
        product_order_ids: List[str],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Confirm order acceptance.

        Args:
            product_order_ids: List of product order IDs to confirm
            **kwargs: Additional parameters

        Returns:
            Confirmation response
        """
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
        }
        body.update(kwargs)

        return await self._post(
            "/v1/orders/confirm",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def ship(
        self,
        *,
        product_order_ids: List[str],
        shipping_company: str,
        tracking_number: str,
        shipping_date: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Register shipping information for orders.

        Args:
            product_order_ids: List of product order IDs to ship
            shipping_company: Shipping company name
            tracking_number: Tracking/invoice number
            shipping_date: Shipping date (YYYY-MM-DD format)
            **kwargs: Additional parameters

        Returns:
            Shipping registration response
        """
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
            "deliveryCompany": shipping_company,
            "trackingNumber": tracking_number,
        }

        if not isinstance(shipping_date, NotGiven):
            body["shippingDate"] = shipping_date

        body.update(kwargs)

        return await self._post(
            "/v1/orders/ship",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def cancel(
        self,
        *,
        product_order_ids: List[str],
        cancel_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Cancel orders.

        Args:
            product_order_ids: List of product order IDs to cancel
            cancel_reason: Reason for cancellation
            **kwargs: Additional parameters

        Returns:
            Cancellation response
        """
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
            "cancelReason": cancel_reason,
        }
        body.update(kwargs)

        return await self._post(
            "/v1/orders/cancel",
            cast_to=dict,  # type: ignore
            body=body,
        )
