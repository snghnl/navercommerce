"""Commerce Solutions resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given
from ...types.commerce_solutions import (
    SellerInfo,
    SubscriptionResponse,
    TransactionResponse,
)

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class CommerceSolutions(SyncAPIResource):
    """
    Commerce Solutions resource for partner integrations.

    This resource provides access to:
    - Subscription management (approve, reject, unsubscribe)
    - Seller JWT token decoding
    - Wallet transaction management
    """

    def approve_subscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Approve a subscription request.

        Args:
            account_uid: Account UID
            **kwargs: Additional parameters

        Returns:
            Approval response

        Example:
            ```python
            result = client.commerce_solutions.approve_subscription(
                account_uid="12345"
            )
            ```
        """
        body: Dict[str, Any] = {
            "accountUid": account_uid,
        }
        body.update(kwargs)

        return self._put(
            "/v1/commerce-solutions/subscriptions/approve",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def reject_subscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Reject a subscription request.

        Args:
            account_uid: Account UID
            **kwargs: Additional parameters

        Returns:
            Rejection response

        Example:
            ```python
            result = client.commerce_solutions.reject_subscription(
                account_uid="12345"
            )
            ```
        """
        body: Dict[str, Any] = {}
        body.update(kwargs)

        return self._put(
            f"/v1/commerce-solutions/subscriptions/{account_uid}/reject",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def request_unsubscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Request unsubscription.

        Args:
            account_uid: Account UID
            **kwargs: Additional parameters

        Returns:
            Unsubscription request response

        Example:
            ```python
            result = client.commerce_solutions.request_unsubscription(
                account_uid="12345"
            )
            ```
        """
        body: Dict[str, Any] = {}
        body.update(kwargs)

        return self._put(
            f"/v1/commerce-solutions/subscriptions/{account_uid}/unsubscription",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def approve_unsubscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Approve an unsubscription request.

        Args:
            account_uid: Account UID
            **kwargs: Additional parameters

        Returns:
            Approval response

        Example:
            ```python
            result = client.commerce_solutions.approve_unsubscription(
                account_uid="12345"
            )
            ```
        """
        body: Dict[str, Any] = {
            "accountUid": account_uid,
        }
        body.update(kwargs)

        return self._put(
            "/v1/commerce-solutions/subscriptions/unsubscription/approve",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def get_subscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> SubscriptionResponse:
        """
        Get subscription status.

        Args:
            account_uid: Account UID
            **kwargs: Additional query parameters

        Returns:
            SubscriptionResponse with subscription details

        Example:
            ```python
            subscription = client.commerce_solutions.get_subscription(
                account_uid="12345"
            )
            print(f"Status: {subscription.subscription.status}")
            ```
        """
        return self._get(
            f"/v1/commerce-solutions/subscriptions/{account_uid}",
            cast_to=SubscriptionResponse,
            options={"params": kwargs},
        )

    def get_seller_info_from_token(
        self,
        *,
        token: str,
        **kwargs: Any,
    ) -> SellerInfo:
        """
        Decode seller JWT token.

        Args:
            token: JWT token to decode
            **kwargs: Additional query parameters

        Returns:
            SellerInfo with decoded information

        Example:
            ```python
            seller_info = client.commerce_solutions.get_seller_info_from_token(
                token="eyJhbGciOiJI..."
            )
            print(f"Seller ID: {seller_info.seller_id}")
            ```
        """
        params: Dict[str, Any] = {
            "token": token,
        }
        params.update(kwargs)

        return self._get(
            "/v1/commerce-solutions/seller-info-by-token",
            cast_to=SellerInfo,
            options={"params": params},
        )

    def list_transactions(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> TransactionResponse:
        """
        List wallet transactions.

        Args:
            page: Page number
            size: Page size
            **kwargs: Additional query parameters

        Returns:
            TransactionResponse with transaction list

        Example:
            ```python
            transactions = client.commerce_solutions.list_transactions(
                page=0,
                size=20
            )
            for txn in transactions.transactions:
                print(f"Transaction: {txn.transaction_type} - {txn.amount}")
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/commerce-solutions/transactions",
            cast_to=TransactionResponse,
            options={"params": params},
        )

    def create_external_transaction(
        self,
        *,
        transaction_type: str,
        amount: int,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Record an external transaction.

        Args:
            transaction_type: Transaction type
            amount: Transaction amount
            **kwargs: Additional parameters

        Returns:
            Creation response

        Example:
            ```python
            result = client.commerce_solutions.create_external_transaction(
                transaction_type="PAYMENT",
                amount=10000
            )
            ```
        """
        body: Dict[str, Any] = {
            "transactionType": transaction_type,
            "amount": amount,
        }
        body.update(kwargs)

        return self._post(
            "/v1/commerce-solutions/external-transactions",
            cast_to=dict,  # type: ignore
            body=body,
        )


class AsyncCommerceSolutions(AsyncAPIResource):
    """
    Async Commerce Solutions resource for partner integrations.

    This resource provides async access to:
    - Subscription management
    - Seller JWT token decoding
    - Wallet transaction management
    """

    async def approve_subscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Approve a subscription request."""
        body: Dict[str, Any] = {
            "accountUid": account_uid,
        }
        body.update(kwargs)

        return await self._put(
            "/v1/commerce-solutions/subscriptions/approve",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def reject_subscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Reject a subscription request."""
        body: Dict[str, Any] = {}
        body.update(kwargs)

        return await self._put(
            f"/v1/commerce-solutions/subscriptions/{account_uid}/reject",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def request_unsubscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Request unsubscription."""
        body: Dict[str, Any] = {}
        body.update(kwargs)

        return await self._put(
            f"/v1/commerce-solutions/subscriptions/{account_uid}/unsubscription",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def approve_unsubscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Approve an unsubscription request."""
        body: Dict[str, Any] = {
            "accountUid": account_uid,
        }
        body.update(kwargs)

        return await self._put(
            "/v1/commerce-solutions/subscriptions/unsubscription/approve",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def get_subscription(
        self,
        *,
        account_uid: str,
        **kwargs: Any,
    ) -> SubscriptionResponse:
        """Get subscription status."""
        return await self._get(
            f"/v1/commerce-solutions/subscriptions/{account_uid}",
            cast_to=SubscriptionResponse,
            options={"params": kwargs},
        )

    async def get_seller_info_from_token(
        self,
        *,
        token: str,
        **kwargs: Any,
    ) -> SellerInfo:
        """Decode seller JWT token."""
        params: Dict[str, Any] = {
            "token": token,
        }
        params.update(kwargs)

        return await self._get(
            "/v1/commerce-solutions/seller-info-by-token",
            cast_to=SellerInfo,
            options={"params": params},
        )

    async def list_transactions(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> TransactionResponse:
        """List wallet transactions."""
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/commerce-solutions/transactions",
            cast_to=TransactionResponse,
            options={"params": params},
        )

    async def create_external_transaction(
        self,
        *,
        transaction_type: str,
        amount: int,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Record an external transaction."""
        body: Dict[str, Any] = {
            "transactionType": transaction_type,
            "amount": amount,
        }
        body.update(kwargs)

        return await self._post(
            "/v1/commerce-solutions/external-transactions",
            cast_to=dict,  # type: ignore
            body=body,
        )
