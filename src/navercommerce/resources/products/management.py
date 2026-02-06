"""Products management sub-resource implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource

if TYPE_CHECKING:
    pass


class ProductsManagement(SyncAPIResource):
    """
    Products management sub-resource for bulk operations.

    This resource provides access to:
    - Bulk product updates
    - Product status management
    - Stock management
    - Standard options
    """

    def bulk_update(
        self,
        *,
        products: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Bulk update products.

        Args:
            products: List of product update objects
            **kwargs: Additional parameters

        Returns:
            Bulk update response

        Example:
            ```python
            result = client.products.management.bulk_update(
                products=[
                    {"productId": "123", "salePrice": 10000},
                    {"productId": "456", "salePrice": 20000},
                ]
            )
            ```
        """
        body: Dict[str, Any] = {
            "products": products,
        }
        body.update(kwargs)

        return self._put(
            "/v1/products/origin-products/bulk-update",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def change_status(
        self,
        *,
        product_id: str,
        status: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Change product status.

        Args:
            product_id: Product ID
            status: New status (e.g., "SALE", "STOP_SALE")
            **kwargs: Additional parameters

        Returns:
            Status change response

        Example:
            ```python
            result = client.products.management.change_status(
                product_id="123",
                status="SALE"
            )
            ```
        """
        body: Dict[str, Any] = {
            "status": status,
        }
        body.update(kwargs)

        return self._put(
            f"/v1/products/origin-products/{product_id}/change-status",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def update_option_stock(
        self,
        *,
        product_id: str,
        stock_quantity: int,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update product option stock.

        Args:
            product_id: Product ID
            stock_quantity: New stock quantity
            **kwargs: Additional parameters

        Returns:
            Stock update response

        Example:
            ```python
            result = client.products.management.update_option_stock(
                product_id="123",
                stock_quantity=50
            )
            ```
        """
        body: Dict[str, Any] = {
            "stockQuantity": stock_quantity,
        }
        body.update(kwargs)

        return self._put(
            f"/v1/products/origin-products/{product_id}/option-stock",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def multi_update(
        self,
        *,
        updates: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Multi-product update.

        Args:
            updates: List of update objects
            **kwargs: Additional parameters

        Returns:
            Multi-update response

        Example:
            ```python
            result = client.products.management.multi_update(
                updates=[...]
            )
            ```
        """
        body: Dict[str, Any] = {
            "updates": updates,
        }
        body.update(kwargs)

        return self._patch(
            "/v1/products/origin-products/multi-update",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def list_standard_options(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List standard options.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of standard option objects

        Example:
            ```python
            options = client.products.management.list_standard_options()
            ```
        """
        return self._get(
            "/v1/options/standard-options",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def get_purchase_option_guides(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get standard purchase option guides.

        Args:
            **kwargs: Additional query parameters

        Returns:
            Purchase option guides

        Example:
            ```python
            guides = client.products.management.get_purchase_option_guides()
            ```
        """
        return self._get(
            "/v2/standard-purchase-option-guides",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    def apply_channel_notice(
        self,
        *,
        product_id: str,
        notice_data: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Apply channel product notice.

        Args:
            product_id: Product ID
            notice_data: Notice data to apply
            **kwargs: Additional parameters

        Returns:
            Apply response

        Example:
            ```python
            result = client.products.management.apply_channel_notice(
                product_id="123",
                notice_data={...}
            )
            ```
        """
        body: Dict[str, Any] = notice_data.copy()
        body.update(kwargs)

        return self._put(
            "/v1/products/channel-products/notice/apply",
            cast_to=dict,  # type: ignore
            body=body,
        )


class AsyncProductsManagement(AsyncAPIResource):
    """Async products management sub-resource."""

    async def bulk_update(self, *, products: List[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        """Bulk update products."""
        body: Dict[str, Any] = {"products": products}
        body.update(kwargs)
        return await self._put(
            "/v1/products/origin-products/bulk-update",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def change_status(self, *, product_id: str, status: str, **kwargs: Any) -> Dict[str, Any]:
        """Change product status."""
        body: Dict[str, Any] = {"status": status}
        body.update(kwargs)
        return await self._put(
            f"/v1/products/origin-products/{product_id}/change-status",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def update_option_stock(self, *, product_id: str, stock_quantity: int, **kwargs: Any) -> Dict[str, Any]:
        """Update product option stock."""
        body: Dict[str, Any] = {"stockQuantity": stock_quantity}
        body.update(kwargs)
        return await self._put(
            f"/v1/products/origin-products/{product_id}/option-stock",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def multi_update(self, *, updates: List[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        """Multi-product update."""
        body: Dict[str, Any] = {"updates": updates}
        body.update(kwargs)
        return await self._patch(
            "/v1/products/origin-products/multi-update",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def list_standard_options(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List standard options."""
        return await self._get(
            "/v1/options/standard-options",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def get_purchase_option_guides(self, **kwargs: Any) -> Dict[str, Any]:
        """Get standard purchase option guides."""
        return await self._get(
            "/v2/standard-purchase-option-guides",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    async def apply_channel_notice(
        self, *, product_id: str, notice_data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]:
        """Apply channel product notice."""
        body: Dict[str, Any] = notice_data.copy()
        body.update(kwargs)
        return await self._put(
            "/v1/products/channel-products/notice/apply",
            cast_to=dict,  # type: ignore
            body=body,
        )
