"""Products delivery sub-resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given

if TYPE_CHECKING:
    pass


class ProductsDelivery(SyncAPIResource):
    """
    Products delivery sub-resource for delivery settings.

    This resource provides access to:
    - Bundle groups (bundled shipping)
    - Hope delivery groups (requested delivery dates)
    - Return delivery companies
    """

    # Bundle Groups
    def list_bundle_groups(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List bundle groups.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of bundle group objects

        Example:
            ```python
            groups = client.products.delivery.list_bundle_groups()
            ```
        """
        return self._get(
            "/v1/product-delivery-info/bundle-groups",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def get_bundle_group(
        self,
        group_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get bundle group by ID.

        Args:
            group_id: Bundle group ID
            **kwargs: Additional query parameters

        Returns:
            Bundle group object

        Example:
            ```python
            group = client.products.delivery.get_bundle_group("123")
            ```
        """
        return self._get(
            f"/v1/product-delivery-info/bundle-groups/{group_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    def create_bundle_group(
        self,
        *,
        name: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a bundle group.

        Args:
            name: Bundle group name
            **kwargs: Additional parameters

        Returns:
            Created bundle group

        Example:
            ```python
            group = client.products.delivery.create_bundle_group(
                name="Electronics Bundle"
            )
            ```
        """
        body: Dict[str, Any] = {
            "name": name,
        }
        body.update(kwargs)

        return self._post(
            "/v1/product-delivery-info/bundle-groups",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def update_bundle_group(
        self,
        *,
        group_id: str,
        name: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update a bundle group.

        Args:
            group_id: Bundle group ID
            name: Bundle group name
            **kwargs: Additional parameters

        Returns:
            Updated bundle group

        Example:
            ```python
            group = client.products.delivery.update_bundle_group(
                group_id="123",
                name="Updated Name"
            )
            ```
        """
        body: Dict[str, Any] = {}

        if not isinstance(name, NotGiven):
            body["name"] = name

        body.update(kwargs)

        return self._put(
            f"/v1/product-delivery-info/bundle-groups/{group_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    # Hope Delivery Groups
    def list_hope_delivery_groups(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List hope delivery groups (requested delivery dates).

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of hope delivery group objects

        Example:
            ```python
            groups = client.products.delivery.list_hope_delivery_groups()
            ```
        """
        return self._get(
            "/v1/product-delivery-info/hope-delivery-groups",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def get_hope_delivery_group(
        self,
        group_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get hope delivery group by ID.

        Args:
            group_id: Hope delivery group ID
            **kwargs: Additional query parameters

        Returns:
            Hope delivery group object

        Example:
            ```python
            group = client.products.delivery.get_hope_delivery_group("123")
            ```
        """
        return self._get(
            f"/v1/product-delivery-info/hope-delivery-groups/{group_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    def create_hope_delivery_group(
        self,
        *,
        name: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a hope delivery group.

        Args:
            name: Hope delivery group name
            **kwargs: Additional parameters

        Returns:
            Created hope delivery group

        Example:
            ```python
            group = client.products.delivery.create_hope_delivery_group(
                name="Express Delivery"
            )
            ```
        """
        body: Dict[str, Any] = {
            "name": name,
        }
        body.update(kwargs)

        return self._post(
            "/v1/product-delivery-info/hope-delivery-groups",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def update_hope_delivery_group(
        self,
        *,
        group_id: str,
        name: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update a hope delivery group.

        Args:
            group_id: Hope delivery group ID
            name: Hope delivery group name
            **kwargs: Additional parameters

        Returns:
            Updated hope delivery group

        Example:
            ```python
            group = client.products.delivery.update_hope_delivery_group(
                group_id="123",
                name="Updated Name"
            )
            ```
        """
        body: Dict[str, Any] = {}

        if not isinstance(name, NotGiven):
            body["name"] = name

        body.update(kwargs)

        return self._put(
            f"/v1/product-delivery-info/hope-delivery-groups/{group_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    # Return Delivery Companies
    def list_return_companies(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List return delivery companies.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of return delivery company objects

        Example:
            ```python
            companies = client.products.delivery.list_return_companies()
            ```
        """
        return self._get(
            "/v2/product-delivery-info/return-delivery-companies",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )


class AsyncProductsDelivery(AsyncAPIResource):
    """Async products delivery sub-resource."""

    async def list_bundle_groups(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List bundle groups."""
        return await self._get(
            "/v1/product-delivery-info/bundle-groups",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def get_bundle_group(self, group_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Get bundle group by ID."""
        return await self._get(
            f"/v1/product-delivery-info/bundle-groups/{group_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    async def create_bundle_group(self, *, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Create a bundle group."""
        body: Dict[str, Any] = {"name": name}
        body.update(kwargs)
        return await self._post(
            "/v1/product-delivery-info/bundle-groups",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def update_bundle_group(
        self, *, group_id: str, name: str | NotGiven = not_given, **kwargs: Any
    ) -> Dict[str, Any]:
        """Update a bundle group."""
        body: Dict[str, Any] = {}
        if not isinstance(name, NotGiven):
            body["name"] = name
        body.update(kwargs)
        return await self._put(
            f"/v1/product-delivery-info/bundle-groups/{group_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def list_hope_delivery_groups(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List hope delivery groups."""
        return await self._get(
            "/v1/product-delivery-info/hope-delivery-groups",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def get_hope_delivery_group(self, group_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Get hope delivery group by ID."""
        return await self._get(
            f"/v1/product-delivery-info/hope-delivery-groups/{group_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    async def create_hope_delivery_group(self, *, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Create a hope delivery group."""
        body: Dict[str, Any] = {"name": name}
        body.update(kwargs)
        return await self._post(
            "/v1/product-delivery-info/hope-delivery-groups",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def update_hope_delivery_group(
        self, *, group_id: str, name: str | NotGiven = not_given, **kwargs: Any
    ) -> Dict[str, Any]:
        """Update a hope delivery group."""
        body: Dict[str, Any] = {}
        if not isinstance(name, NotGiven):
            body["name"] = name
        body.update(kwargs)
        return await self._put(
            f"/v1/product-delivery-info/hope-delivery-groups/{group_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def list_return_companies(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List return delivery companies."""
        return await self._get(
            "/v2/product-delivery-info/return-delivery-companies",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )
