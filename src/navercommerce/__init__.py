"""
Naver Commerce SDK for Python

A production-grade Python SDK for the Naver Commerce API.

Example:
    Basic usage:
    ```python
    from navercommerce import NaverCommerce

    client = NaverCommerce(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Get seller info
    account = client.seller.account()
    print(f"Seller: {account.seller_name}")
    ```

    Async usage:
    ```python
    import asyncio
    from navercommerce import AsyncNaverCommerce

    async def main():
        async with AsyncNaverCommerce(
            client_id="your_client_id",
            client_secret="your_client_secret"
        ) as client:
            account = await client.seller.account()
            print(f"Seller: {account.seller_name}")

    asyncio.run(main())
    ```
"""

from ._client import AsyncNaverCommerce, NaverCommerce
from ._exceptions import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NaverCommerceError,
    NotFoundError,
    OAuthError,
    PermissionDeniedError,
    TokenExpiredError,
    TokenRefreshError,
)

__version__ = "0.1.0"

__all__ = [
    # Main clients
    "NaverCommerce",
    "AsyncNaverCommerce",
    # Exceptions
    "NaverCommerceError",
    "APIError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "InternalServerError",
    "OAuthError",
    "TokenExpiredError",
    "TokenRefreshError",
    # Version
    "__version__",
]
