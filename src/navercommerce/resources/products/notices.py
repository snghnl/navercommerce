"""Products notices sub-resource implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class ProductsNotices(SyncAPIResource):
    """
    Products notices sub-resource for product information notices.

    This resource provides access to product notice types.
    """

    def list_types(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List product notice types.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of product notice type objects

        Example:
            ```python
            types = client.products.notices.list_types()
            ```
        """
        return self._get(
            "/v1/products-for-provided-notice",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def get_type(
        self,
        notice_type: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get product notice type.

        Args:
            notice_type: Notice type identifier
            **kwargs: Additional query parameters

        Returns:
            Product notice type object

        Example:
            ```python
            notice_type = client.products.notices.get_type("ELECTRONICS")
            ```
        """
        return self._get(
            f"/v1/products-for-provided-notice/{notice_type}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )


class AsyncProductsNotices(AsyncAPIResource):
    """Async products notices sub-resource."""

    async def list_types(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List product notice types."""
        return await self._get(
            "/v1/products-for-provided-notice",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def get_type(self, notice_type: str, **kwargs: Any) -> Dict[str, Any]:
        """Get product notice type."""
        return await self._get(
            f"/v1/products-for-provided-notice/{notice_type}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )
