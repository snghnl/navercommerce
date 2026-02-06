"""Main client classes for the Naver Commerce SDK."""

from __future__ import annotations

import os
from functools import cached_property
from typing import Any

from ._base_client import AsyncAPIClient, SyncAPIClient
from ._constants import BASE_URL, ENV_CLIENT_ID, ENV_CLIENT_SECRET
from ._types import Timeout


class NaverCommerce(SyncAPIClient):
    """
    Synchronous client for the Naver Commerce API.

    This is the main entry point for interacting with the Naver Commerce API.
    It provides access to all API resources through lazy-loaded properties.

    Args:
        client_id: Naver Commerce API client ID. If not provided, will read from
            NAVER_CLIENT_ID environment variable.
        client_secret: Naver Commerce API client secret. If not provided, will read from
            NAVER_CLIENT_SECRET environment variable.
        base_url: Base URL for the API. Defaults to the production API URL.
        timeout: Request timeout in seconds. Defaults to 60 seconds.
        max_retries: Maximum number of retry attempts. Defaults to 2.

    Example:
        Basic usage:
        ```python
        from navercommerce import NaverCommerce

        client = NaverCommerce(
            client_id="your_client_id",
            client_secret="your_client_secret"
        )

        # Get seller account info
        account = client.seller.account()
        print(f"Seller: {account.name}")

        # List products
        products = client.products.list(page=1, size=10)
        for product in products:
            print(f"Product: {product.name}")
        ```

    Environment variables:
        NAVER_CLIENT_ID: Client ID for authentication
        NAVER_CLIENT_SECRET: Client secret for authentication
    """

    def __init__(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str = BASE_URL,
        timeout: Timeout = None,
        max_retries: int = 2,
        **kwargs: Any,
    ) -> None:
        # Read credentials from environment if not provided
        if client_id is None:
            client_id = os.environ.get(ENV_CLIENT_ID)
        if client_secret is None:
            client_secret = os.environ.get(ENV_CLIENT_SECRET)

        # Validate credentials
        if not client_id:
            raise ValueError(f"Client ID is required. Pass client_id or set {ENV_CLIENT_ID} environment variable.")
        if not client_secret:
            raise ValueError(
                f"Client secret is required. Pass client_secret or set {ENV_CLIENT_SECRET} environment variable."
            )

        # Initialize the base client
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs,
        )

    @cached_property
    def products(self) -> Any:
        """
        Access the Products resource.

        Returns:
            Products resource for managing products, categories, and brands.
        """
        from .resources.products import Products

        return Products(self)

    @cached_property
    def orders(self) -> Any:
        """
        Access the Orders resource.

        Returns:
            Orders resource for managing orders, confirmations, and shipping.
        """
        from .resources.orders import Orders

        return Orders(self)

    @cached_property
    def seller(self) -> Any:
        """
        Access the Seller resource.

        Returns:
            Seller resource for accessing account info, channels, and address book.
        """
        from .resources.seller import Seller

        return Seller(self)

    @cached_property
    def settlement(self) -> Any:
        """
        Access the Settlement resource.

        Returns:
            Settlement resource for financial reporting and commission details.
        """
        from .resources.settlement import Settlement

        return Settlement(self)

    @cached_property
    def inquiries(self) -> Any:
        """
        Access the Inquiries resource.

        Returns:
            Inquiries resource for managing Q&As and seller notices.
        """
        from .resources.inquiries import Inquiries

        return Inquiries(self)

    @cached_property
    def commerce_solutions(self) -> Any:
        """
        Access the Commerce Solutions resource.

        Returns:
            Commerce Solutions resource for subscription and transaction management.
        """
        from .resources.commerce_solutions import CommerceSolutions

        return CommerceSolutions(self)

    @cached_property
    def analytics(self) -> Any:
        """
        Access the Analytics resource.

        Returns:
            Analytics resource for marketing and sales performance data.
        """
        from .resources.analytics import Analytics

        return Analytics(self)


class AsyncNaverCommerce(AsyncAPIClient):
    """
    Asynchronous client for the Naver Commerce API.

    This is the main entry point for asynchronously interacting with the Naver Commerce API.
    It provides access to all API resources through lazy-loaded properties.

    Args:
        client_id: Naver Commerce API client ID. If not provided, will read from
            NAVER_CLIENT_ID environment variable.
        client_secret: Naver Commerce API client secret. If not provided, will read from
            NAVER_CLIENT_SECRET environment variable.
        base_url: Base URL for the API. Defaults to the production API URL.
        timeout: Request timeout in seconds. Defaults to 60 seconds.
        max_retries: Maximum number of retry attempts. Defaults to 2.

    Example:
        Basic async usage:
        ```python
        import asyncio
        from navercommerce import AsyncNaverCommerce

        async def main():
            async with AsyncNaverCommerce(
                client_id="your_client_id",
                client_secret="your_client_secret"
            ) as client:
                # Get seller account info
                account = await client.seller.account()
                print(f"Seller: {account.name}")

                # List products
                products = await client.products.list(page=1, size=10)
                for product in products:
                    print(f"Product: {product.name}")

        asyncio.run(main())
        ```

    Environment variables:
        NAVER_CLIENT_ID: Client ID for authentication
        NAVER_CLIENT_SECRET: Client secret for authentication
    """

    def __init__(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str = BASE_URL,
        timeout: Timeout = None,
        max_retries: int = 2,
        **kwargs: Any,
    ) -> None:
        # Read credentials from environment if not provided
        if client_id is None:
            client_id = os.environ.get(ENV_CLIENT_ID)
        if client_secret is None:
            client_secret = os.environ.get(ENV_CLIENT_SECRET)

        # Validate credentials
        if not client_id:
            raise ValueError(f"Client ID is required. Pass client_id or set {ENV_CLIENT_ID} environment variable.")
        if not client_secret:
            raise ValueError(
                f"Client secret is required. Pass client_secret or set {ENV_CLIENT_SECRET} environment variable."
            )

        # Initialize the base client
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs,
        )

    @cached_property
    def products(self) -> Any:
        """
        Access the Products resource.

        Returns:
            Async Products resource for managing products, categories, and brands.
        """
        from .resources.products import AsyncProducts

        return AsyncProducts(self)

    @cached_property
    def orders(self) -> Any:
        """
        Access the Orders resource.

        Returns:
            Async Orders resource for managing orders, confirmations, and shipping.
        """
        from .resources.orders import AsyncOrders

        return AsyncOrders(self)

    @cached_property
    def seller(self) -> Any:
        """
        Access the Seller resource.

        Returns:
            Async Seller resource for accessing account info, channels, and address book.
        """
        from .resources.seller import AsyncSeller

        return AsyncSeller(self)

    @cached_property
    def settlement(self) -> Any:
        """
        Access the Settlement resource.

        Returns:
            Async Settlement resource for financial reporting and commission details.
        """
        from .resources.settlement import AsyncSettlement

        return AsyncSettlement(self)

    @cached_property
    def inquiries(self) -> Any:
        """
        Access the Inquiries resource.

        Returns:
            Async Inquiries resource for managing Q&As and seller notices.
        """
        from .resources.inquiries import AsyncInquiries

        return AsyncInquiries(self)

    @cached_property
    def commerce_solutions(self) -> Any:
        """
        Access the Commerce Solutions resource.

        Returns:
            Async Commerce Solutions resource for subscription and transaction management.
        """
        from .resources.commerce_solutions import AsyncCommerceSolutions

        return AsyncCommerceSolutions(self)

    @cached_property
    def analytics(self) -> Any:
        """
        Access the Analytics resource.

        Returns:
            Async Analytics resource for marketing and sales performance data.
        """
        from .resources.analytics import AsyncAnalytics

        return AsyncAnalytics(self)
