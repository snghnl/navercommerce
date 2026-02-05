"""Orders resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

import warnings
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
            "/v1/pay-order/seller/product-orders/query",
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
        # NOTE: The API uses POST with productOrderIds array for retrieval
        body = {"productOrderIds": [product_order_id]}
        result = self._post(
            "/v1/pay-order/seller/product-orders/query",
            cast_to=List[OrderProductInfo],  # type: ignore
            body=body,
        )
        # Return first result if available
        if result and len(result) > 0:
            # Convert OrderProductInfo to Order if needed
            return result[0]  # type: ignore
        raise ValueError(f"Order {product_order_id} not found")

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
            "/v1/pay-order/seller/product-orders/confirm",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def dispatch(
        self,
        *,
        dispatch_product_orders: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Dispatch (ship) product orders.

        Args:
            dispatch_product_orders: List of dispatch order objects with fields:
                - productOrderId: Product order ID
                - deliveryMethod: Delivery method (e.g., "DELIVERY")
                - deliveryCompanyCode: Delivery company code
                - trackingNumber: Tracking number
                - dispatchDate: Dispatch date (ISO 8601 format)
            **kwargs: Additional parameters

        Returns:
            Dispatch response

        Example:
            ```python
            result = client.orders.dispatch(
                dispatch_product_orders=[{
                    "productOrderId": "2024010112345678",
                    "deliveryMethod": "DELIVERY",
                    "deliveryCompanyCode": "CJGLS",
                    "trackingNumber": "123456789012",
                    "dispatchDate": "2024-01-15T10:00:00.000+09:00"
                }]
            )
            ```
        """
        body: Dict[str, Any] = {
            "dispatchProductOrders": dispatch_product_orders,
        }
        body.update(kwargs)

        return self._post(
            "/v1/pay-order/seller/product-orders/dispatch",
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
        DEPRECATED: Use dispatch() instead.

        Register shipping information for orders.

        Args:
            product_order_ids: List of product order IDs to ship
            shipping_company: Shipping company name (e.g., "CJ대한통운", "우체국택배")
            tracking_number: Tracking/invoice number
            shipping_date: Shipping date (YYYY-MM-DD format)
            **kwargs: Additional parameters

        Returns:
            Shipping registration response
        """
        warnings.warn(
            "ship() is deprecated. Use dispatch() instead with the new API format. "
            "This method will be removed in v2.0.0.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Convert old format to new dispatch format
        dispatch_orders = []
        for product_order_id in product_order_ids:
            dispatch_order: Dict[str, Any] = {
                "productOrderId": product_order_id,
                "deliveryMethod": "DELIVERY",
                "deliveryCompanyCode": shipping_company,
                "trackingNumber": tracking_number,
            }
            if not isinstance(shipping_date, NotGiven):
                dispatch_order["dispatchDate"] = f"{shipping_date}T00:00:00.000+09:00"
            dispatch_orders.append(dispatch_order)

        return self.dispatch(dispatch_product_orders=dispatch_orders, **kwargs)

    def cancel_request(
        self,
        *,
        product_order_id: str,
        cancel_reason: str,
        cancel_detailed_reason: str | NotGiven = not_given,
        cancel_quantity: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Request cancellation for a product order.

        Note: This is a two-step process. After requesting cancellation,
        you must call cancel_approve() to complete the cancellation.

        Args:
            product_order_id: Product order ID to cancel
            cancel_reason: Reason for cancellation
            cancel_detailed_reason: Detailed reason for cancellation
            cancel_quantity: Quantity to cancel (for partial cancellations)
            **kwargs: Additional parameters

        Returns:
            Cancellation request response

        Example:
            ```python
            result = client.orders.cancel_request(
                product_order_id="2024010112345678",
                cancel_reason="SOLD_OUT",
                cancel_detailed_reason="Out of stock"
            )
            ```
        """
        body: Dict[str, Any] = {
            "cancelReason": cancel_reason,
        }

        if not isinstance(cancel_detailed_reason, NotGiven):
            body["cancelDetailedReason"] = cancel_detailed_reason
        if not isinstance(cancel_quantity, NotGiven):
            body["cancelQuantity"] = cancel_quantity

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/cancel/request",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def cancel_approve(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Approve a cancellation request.

        This completes the cancellation process started with cancel_request().

        Args:
            product_order_id: Product order ID
            **kwargs: Additional parameters

        Returns:
            Cancellation approval response

        Example:
            ```python
            result = client.orders.cancel_approve(
                product_order_id="2024010112345678"
            )
            ```
        """
        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/cancel/approve",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    def cancel(
        self,
        *,
        product_order_ids: List[str],
        cancel_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        DEPRECATED: Use cancel_request() + cancel_approve() instead.

        Cancel orders.

        Args:
            product_order_ids: List of product order IDs to cancel
            cancel_reason: Reason for cancellation
            **kwargs: Additional parameters

        Returns:
            Cancellation response
        """
        warnings.warn(
            "cancel() is deprecated. The API now requires a two-step workflow: "
            "cancel_request() followed by cancel_approve(). "
            "This method will be removed in v2.0.0.",
            DeprecationWarning,
            stacklevel=2,
        )

        # For backward compatibility, request cancellation for all orders
        results = []
        for product_order_id in product_order_ids:
            result = self.cancel_request(
                product_order_id=product_order_id,
                cancel_reason=cancel_reason,
                **kwargs,
            )
            results.append(result)
        return {"results": results}

    # Return Management Methods
    def return_request(
        self,
        *,
        product_order_id: str,
        return_reason: str,
        collect_delivery_method: str | NotGiven = not_given,
        collect_delivery_company: str | NotGiven = not_given,
        collect_tracking_number: str | NotGiven = not_given,
        return_quantity: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Request a product return.

        Args:
            product_order_id: Product order ID
            return_reason: Reason for return
            collect_delivery_method: Collection delivery method
            collect_delivery_company: Collection delivery company
            collect_tracking_number: Collection tracking number
            return_quantity: Quantity to return
            **kwargs: Additional parameters

        Returns:
            Return request response

        Example:
            ```python
            result = client.orders.return_request(
                product_order_id="2024010112345678",
                return_reason="WRONG_PRODUCT",
                collect_delivery_method="DELIVERY",
                collect_delivery_company="CJGLS",
                collect_tracking_number="987654321"
            )
            ```
        """
        body: Dict[str, Any] = {
            "returnReason": return_reason,
        }

        if not isinstance(collect_delivery_method, NotGiven):
            body["collectDeliveryMethod"] = collect_delivery_method
        if not isinstance(collect_delivery_company, NotGiven):
            body["collectDeliveryCompany"] = collect_delivery_company
        if not isinstance(collect_tracking_number, NotGiven):
            body["collectTrackingNumber"] = collect_tracking_number
        if not isinstance(return_quantity, NotGiven):
            body["returnQuantity"] = return_quantity

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/request",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def return_approve(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Approve a return after receiving the returned product.

        Args:
            product_order_id: Product order ID
            **kwargs: Additional parameters

        Returns:
            Return approval response

        Example:
            ```python
            result = client.orders.return_approve(
                product_order_id="2024010112345678"
            )
            ```
        """
        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/approve",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    def return_reject(
        self,
        *,
        product_order_id: str,
        reject_return_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Reject a return request.

        Args:
            product_order_id: Product order ID
            reject_return_reason: Reason for rejecting the return
            **kwargs: Additional parameters

        Returns:
            Return rejection response

        Example:
            ```python
            result = client.orders.return_reject(
                product_order_id="2024010112345678",
                reject_return_reason="Product has been used"
            )
            ```
        """
        body: Dict[str, Any] = {
            "rejectReturnReason": reject_return_reason,
        }
        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/reject",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def return_holdback(
        self,
        *,
        product_order_id: str,
        holdback_class_type: str,
        holdback_return_detail_reason: str,
        extra_return_fee_amount: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Withhold payment for a return (e.g., damaged product).

        Args:
            product_order_id: Product order ID
            holdback_class_type: Type of holdback
            holdback_return_detail_reason: Detailed reason for holdback
            extra_return_fee_amount: Additional return fee amount
            **kwargs: Additional parameters

        Returns:
            Return holdback response

        Example:
            ```python
            result = client.orders.return_holdback(
                product_order_id="2024010112345678",
                holdback_class_type="PRODUCT_DAMAGE",
                holdback_return_detail_reason="Product arrived damaged",
                extra_return_fee_amount=5000
            )
            ```
        """
        body: Dict[str, Any] = {
            "holdbackClassType": holdback_class_type,
            "holdbackReturnDetailReason": holdback_return_detail_reason,
        }

        if not isinstance(extra_return_fee_amount, NotGiven):
            body["extraReturnFeeAmount"] = extra_return_fee_amount

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/holdback",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def return_holdback_release(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Release held payment for a return.

        Args:
            product_order_id: Product order ID
            **kwargs: Additional parameters

        Returns:
            Holdback release response

        Example:
            ```python
            result = client.orders.return_holdback_release(
                product_order_id="2024010112345678"
            )
            ```
        """
        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/holdback/release",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    # Exchange Management Methods
    def exchange_collect_approve(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Approve exchange collection (after receiving the returned product).

        Args:
            product_order_id: Product order ID
            **kwargs: Additional parameters

        Returns:
            Exchange collection approval response

        Example:
            ```python
            result = client.orders.exchange_collect_approve(
                product_order_id="2024010112345678"
            )
            ```
        """
        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/collect/approve",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    def exchange_dispatch(
        self,
        *,
        product_order_id: str,
        re_delivery_method: str,
        re_delivery_company: str | NotGiven = not_given,
        re_delivery_tracking_number: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Dispatch the replacement product for an exchange.

        Args:
            product_order_id: Product order ID
            re_delivery_method: Re-delivery method
            re_delivery_company: Re-delivery company
            re_delivery_tracking_number: Re-delivery tracking number
            **kwargs: Additional parameters

        Returns:
            Exchange dispatch response

        Example:
            ```python
            result = client.orders.exchange_dispatch(
                product_order_id="2024010112345678",
                re_delivery_method="DELIVERY",
                re_delivery_company="CJGLS",
                re_delivery_tracking_number="123456789"
            )
            ```
        """
        body: Dict[str, Any] = {
            "reDeliveryMethod": re_delivery_method,
        }

        if not isinstance(re_delivery_company, NotGiven):
            body["reDeliveryCompany"] = re_delivery_company
        if not isinstance(re_delivery_tracking_number, NotGiven):
            body["reDeliveryTrackingNumber"] = re_delivery_tracking_number

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/dispatch",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def exchange_reject(
        self,
        *,
        product_order_id: str,
        reject_exchange_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Reject an exchange request.

        Args:
            product_order_id: Product order ID
            reject_exchange_reason: Reason for rejecting the exchange
            **kwargs: Additional parameters

        Returns:
            Exchange rejection response

        Example:
            ```python
            result = client.orders.exchange_reject(
                product_order_id="2024010112345678",
                reject_exchange_reason="Product has been worn"
            )
            ```
        """
        body: Dict[str, Any] = {
            "rejectExchangeReason": reject_exchange_reason,
        }
        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/reject",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def exchange_holdback(
        self,
        *,
        product_order_id: str,
        holdback_class_type: str,
        holdback_exchange_detail_reason: str,
        extra_exchange_fee_amount: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Withhold payment for an exchange.

        Args:
            product_order_id: Product order ID
            holdback_class_type: Type of holdback
            holdback_exchange_detail_reason: Detailed reason for holdback
            extra_exchange_fee_amount: Additional exchange fee amount
            **kwargs: Additional parameters

        Returns:
            Exchange holdback response

        Example:
            ```python
            result = client.orders.exchange_holdback(
                product_order_id="2024010112345678",
                holdback_class_type="PRODUCT_DAMAGE",
                holdback_exchange_detail_reason="Product damaged",
                extra_exchange_fee_amount=5000
            )
            ```
        """
        body: Dict[str, Any] = {
            "holdbackClassType": holdback_class_type,
            "holdbackExchangeDetailReason": holdback_exchange_detail_reason,
        }

        if not isinstance(extra_exchange_fee_amount, NotGiven):
            body["extraExchangeFeeAmount"] = extra_exchange_fee_amount

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/holdback",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def exchange_holdback_release(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Release held payment for an exchange.

        Args:
            product_order_id: Product order ID
            **kwargs: Additional parameters

        Returns:
            Holdback release response

        Example:
            ```python
            result = client.orders.exchange_holdback_release(
                product_order_id="2024010112345678"
            )
            ```
        """
        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/holdback/release",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    # Advanced Features
    def list_last_changed_statuses(
        self,
        **kwargs: Any,
    ) -> List[OrderProductInfo]:
        """
        Query product orders by last status change date.

        Args:
            **kwargs: Query parameters including date ranges

        Returns:
            List of OrderProductInfo objects

        Example:
            ```python
            orders = client.orders.list_last_changed_statuses()
            for order in orders:
                print(f"Order: {order.product_order_id}")
            ```
        """
        return self._get(
            "/v1/pay-order/seller/product-orders/last-changed-statuses",
            cast_to=List[OrderProductInfo],  # type: ignore
            options={"params": kwargs},
        )

    def notify_delay(
        self,
        *,
        product_order_id: str,
        dispatch_due_date: str,
        delayed_dispatch_reason: str,
        dispatch_delayed_detailed_reason: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Notify customer of shipping delay.

        Args:
            product_order_id: Product order ID
            dispatch_due_date: New expected dispatch date (ISO 8601 format)
            delayed_dispatch_reason: Reason code for delay
            dispatch_delayed_detailed_reason: Detailed reason for delay
            **kwargs: Additional parameters

        Returns:
            Delay notification response

        Example:
            ```python
            result = client.orders.notify_delay(
                product_order_id="2024010112345678",
                dispatch_due_date="2024-06-05T12:17:35.000+09:00",
                delayed_dispatch_reason="PRODUCT_PREPARE",
                dispatch_delayed_detailed_reason="Product preparation in progress"
            )
            ```
        """
        body: Dict[str, Any] = {
            "dispatchDueDate": dispatch_due_date,
            "delayedDispatchReason": delayed_dispatch_reason,
        }

        if not isinstance(dispatch_delayed_detailed_reason, NotGiven):
            body["dispatchDelayedDetailedReason"] = dispatch_delayed_detailed_reason

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/delay",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def change_hope_delivery(
        self,
        *,
        product_order_id: str,
        hope_delivery_ymd: str,
        hope_delivery_hm: str | NotGiven = not_given,
        region: str | NotGiven = not_given,
        change_reason: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update the requested delivery date for an order.

        Args:
            product_order_id: Product order ID
            hope_delivery_ymd: Desired delivery date (YYYYMMDD format)
            hope_delivery_hm: Desired delivery time (HHMM format)
            region: Delivery region
            change_reason: Reason for changing delivery date
            **kwargs: Additional parameters

        Returns:
            Hope delivery change response

        Example:
            ```python
            result = client.orders.change_hope_delivery(
                product_order_id="2024010112345678",
                hope_delivery_ymd="20221231",
                hope_delivery_hm="1500",
                change_reason="Customer request"
            )
            ```
        """
        body: Dict[str, Any] = {
            "hopeDeliveryYmd": hope_delivery_ymd,
        }

        if not isinstance(hope_delivery_hm, NotGiven):
            body["hopeDeliveryHm"] = hope_delivery_hm
        if not isinstance(region, NotGiven):
            body["region"] = region
        if not isinstance(change_reason, NotGiven):
            body["changeReason"] = change_reason

        body.update(kwargs)

        return self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/hope-delivery/change",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def get_product_order_ids_by_order(
        self,
        *,
        order_id: str,
        **kwargs: Any,
    ) -> List[str]:
        """
        Get all product order IDs for a given order ID.

        Args:
            order_id: Order ID
            **kwargs: Additional parameters

        Returns:
            List of product order IDs

        Example:
            ```python
            product_order_ids = client.orders.get_product_order_ids_by_order(
                order_id="2024010112345678"
            )
            for po_id in product_order_ids:
                print(f"Product Order ID: {po_id}")
            ```
        """
        return self._get(
            f"/v1/pay-order/seller/orders/{order_id}/product-order-ids",
            cast_to=List[str],  # type: ignore
            options={"params": kwargs},
        )


class AsyncOrders(AsyncAPIResource):
    """
    Async orders resource for managing product orders.

    This resource provides async access to:
    - Listing orders by date range
    - Retrieving order details
    - Confirming orders
    - Managing shipping/dispatch information
    - Cancel/return/exchange workflows
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
        """List orders within a date range."""
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
            "/v1/pay-order/seller/product-orders/query",
            cast_to=List[OrderProductInfo],  # type: ignore
            body=body,
        )

    async def retrieve(self, product_order_id: str) -> Order:
        """Retrieve detailed information for a specific order."""
        body = {"productOrderIds": [product_order_id]}
        result = await self._post(
            "/v1/pay-order/seller/product-orders/query",
            cast_to=List[OrderProductInfo],  # type: ignore
            body=body,
        )
        if result and len(result) > 0:
            return result[0]  # type: ignore
        raise ValueError(f"Order {product_order_id} not found")

    async def confirm(
        self,
        *,
        product_order_ids: List[str],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Confirm order acceptance."""
        body: Dict[str, Any] = {
            "productOrderIds": product_order_ids,
        }
        body.update(kwargs)

        return await self._post(
            "/v1/pay-order/seller/product-orders/confirm",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def dispatch(
        self,
        *,
        dispatch_product_orders: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Dispatch (ship) product orders."""
        body: Dict[str, Any] = {
            "dispatchProductOrders": dispatch_product_orders,
        }
        body.update(kwargs)

        return await self._post(
            "/v1/pay-order/seller/product-orders/dispatch",
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
        """DEPRECATED: Use dispatch() instead."""
        warnings.warn(
            "ship() is deprecated. Use dispatch() instead with the new API format. "
            "This method will be removed in v2.0.0.",
            DeprecationWarning,
            stacklevel=2,
        )

        dispatch_orders = []
        for product_order_id in product_order_ids:
            dispatch_order: Dict[str, Any] = {
                "productOrderId": product_order_id,
                "deliveryMethod": "DELIVERY",
                "deliveryCompanyCode": shipping_company,
                "trackingNumber": tracking_number,
            }
            if not isinstance(shipping_date, NotGiven):
                dispatch_order["dispatchDate"] = f"{shipping_date}T00:00:00.000+09:00"
            dispatch_orders.append(dispatch_order)

        return await self.dispatch(dispatch_product_orders=dispatch_orders, **kwargs)

    async def cancel_request(
        self,
        *,
        product_order_id: str,
        cancel_reason: str,
        cancel_detailed_reason: str | NotGiven = not_given,
        cancel_quantity: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Request cancellation for a product order."""
        body: Dict[str, Any] = {
            "cancelReason": cancel_reason,
        }

        if not isinstance(cancel_detailed_reason, NotGiven):
            body["cancelDetailedReason"] = cancel_detailed_reason
        if not isinstance(cancel_quantity, NotGiven):
            body["cancelQuantity"] = cancel_quantity

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/cancel/request",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def cancel_approve(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Approve a cancellation request."""
        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/cancel/approve",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    async def cancel(
        self,
        *,
        product_order_ids: List[str],
        cancel_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """DEPRECATED: Use cancel_request() + cancel_approve() instead."""
        warnings.warn(
            "cancel() is deprecated. The API now requires a two-step workflow: "
            "cancel_request() followed by cancel_approve(). "
            "This method will be removed in v2.0.0.",
            DeprecationWarning,
            stacklevel=2,
        )

        results = []
        for product_order_id in product_order_ids:
            result = await self.cancel_request(
                product_order_id=product_order_id,
                cancel_reason=cancel_reason,
                **kwargs,
            )
            results.append(result)
        return {"results": results}

    # Return Management Methods
    async def return_request(
        self,
        *,
        product_order_id: str,
        return_reason: str,
        collect_delivery_method: str | NotGiven = not_given,
        collect_delivery_company: str | NotGiven = not_given,
        collect_tracking_number: str | NotGiven = not_given,
        return_quantity: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Request a product return."""
        body: Dict[str, Any] = {
            "returnReason": return_reason,
        }

        if not isinstance(collect_delivery_method, NotGiven):
            body["collectDeliveryMethod"] = collect_delivery_method
        if not isinstance(collect_delivery_company, NotGiven):
            body["collectDeliveryCompany"] = collect_delivery_company
        if not isinstance(collect_tracking_number, NotGiven):
            body["collectTrackingNumber"] = collect_tracking_number
        if not isinstance(return_quantity, NotGiven):
            body["returnQuantity"] = return_quantity

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/request",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def return_approve(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Approve a return after receiving the returned product."""
        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/approve",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    async def return_reject(
        self,
        *,
        product_order_id: str,
        reject_return_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Reject a return request."""
        body: Dict[str, Any] = {
            "rejectReturnReason": reject_return_reason,
        }
        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/reject",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def return_holdback(
        self,
        *,
        product_order_id: str,
        holdback_class_type: str,
        holdback_return_detail_reason: str,
        extra_return_fee_amount: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Withhold payment for a return."""
        body: Dict[str, Any] = {
            "holdbackClassType": holdback_class_type,
            "holdbackReturnDetailReason": holdback_return_detail_reason,
        }

        if not isinstance(extra_return_fee_amount, NotGiven):
            body["extraReturnFeeAmount"] = extra_return_fee_amount

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/holdback",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def return_holdback_release(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Release held payment for a return."""
        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/return/holdback/release",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    # Exchange Management Methods
    async def exchange_collect_approve(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Approve exchange collection."""
        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/collect/approve",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    async def exchange_dispatch(
        self,
        *,
        product_order_id: str,
        re_delivery_method: str,
        re_delivery_company: str | NotGiven = not_given,
        re_delivery_tracking_number: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Dispatch the replacement product for an exchange."""
        body: Dict[str, Any] = {
            "reDeliveryMethod": re_delivery_method,
        }

        if not isinstance(re_delivery_company, NotGiven):
            body["reDeliveryCompany"] = re_delivery_company
        if not isinstance(re_delivery_tracking_number, NotGiven):
            body["reDeliveryTrackingNumber"] = re_delivery_tracking_number

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/dispatch",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def exchange_reject(
        self,
        *,
        product_order_id: str,
        reject_exchange_reason: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Reject an exchange request."""
        body: Dict[str, Any] = {
            "rejectExchangeReason": reject_exchange_reason,
        }
        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/reject",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def exchange_holdback(
        self,
        *,
        product_order_id: str,
        holdback_class_type: str,
        holdback_exchange_detail_reason: str,
        extra_exchange_fee_amount: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Withhold payment for an exchange."""
        body: Dict[str, Any] = {
            "holdbackClassType": holdback_class_type,
            "holdbackExchangeDetailReason": holdback_exchange_detail_reason,
        }

        if not isinstance(extra_exchange_fee_amount, NotGiven):
            body["extraExchangeFeeAmount"] = extra_exchange_fee_amount

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/holdback",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def exchange_holdback_release(
        self,
        *,
        product_order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Release held payment for an exchange."""
        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/claim/exchange/holdback/release",
            cast_to=dict,  # type: ignore
            body=kwargs,
        )

    # Advanced Features
    async def list_last_changed_statuses(
        self,
        **kwargs: Any,
    ) -> List[OrderProductInfo]:
        """Query product orders by last status change date."""
        return await self._get(
            "/v1/pay-order/seller/product-orders/last-changed-statuses",
            cast_to=List[OrderProductInfo],  # type: ignore
            options={"params": kwargs},
        )

    async def notify_delay(
        self,
        *,
        product_order_id: str,
        dispatch_due_date: str,
        delayed_dispatch_reason: str,
        dispatch_delayed_detailed_reason: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Notify customer of shipping delay."""
        body: Dict[str, Any] = {
            "dispatchDueDate": dispatch_due_date,
            "delayedDispatchReason": delayed_dispatch_reason,
        }

        if not isinstance(dispatch_delayed_detailed_reason, NotGiven):
            body["dispatchDelayedDetailedReason"] = dispatch_delayed_detailed_reason

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/delay",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def change_hope_delivery(
        self,
        *,
        product_order_id: str,
        hope_delivery_ymd: str,
        hope_delivery_hm: str | NotGiven = not_given,
        region: str | NotGiven = not_given,
        change_reason: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Update the requested delivery date for an order."""
        body: Dict[str, Any] = {
            "hopeDeliveryYmd": hope_delivery_ymd,
        }

        if not isinstance(hope_delivery_hm, NotGiven):
            body["hopeDeliveryHm"] = hope_delivery_hm
        if not isinstance(region, NotGiven):
            body["region"] = region
        if not isinstance(change_reason, NotGiven):
            body["changeReason"] = change_reason

        body.update(kwargs)

        return await self._post(
            f"/v1/pay-order/seller/product-orders/{product_order_id}/hope-delivery/change",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def get_product_order_ids_by_order(
        self,
        *,
        order_id: str,
        **kwargs: Any,
    ) -> List[str]:
        """Get all product order IDs for a given order ID."""
        return await self._get(
            f"/v1/pay-order/seller/orders/{order_id}/product-order-ids",
            cast_to=List[str],  # type: ignore
            options={"params": kwargs},
        )
