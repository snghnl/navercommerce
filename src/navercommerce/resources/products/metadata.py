"""Products metadata sub-resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce


class ProductsMetadata(SyncAPIResource):
    """
    Products metadata sub-resource for product attributes and classifications.

    This resource provides access to:
    - Brands
    - Product attributes (by category)
    - Origin areas
    - Manufacturers
    - Catalog models
    - Size types
    - Fashion models
    """

    # Brands
    def list_brands(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List all product brands.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of brand objects

        Example:
            ```python
            brands = client.products.metadata.list_brands()
            for brand in brands:
                print(f"Brand: {brand}")
            ```
        """
        return self._get(
            "/v1/product-brands",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    # Attributes
    def list_attributes(
        self,
        *,
        category_id: str,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Get category attributes.

        Args:
            category_id: Category ID
            **kwargs: Additional query parameters

        Returns:
            List of attribute objects

        Example:
            ```python
            attrs = client.products.metadata.list_attributes(
                category_id="50000000"
            )
            ```
        """
        params: Dict[str, Any] = {
            "categoryId": category_id,
        }
        params.update(kwargs)

        return self._get(
            "/v1/product-attributes/attributes",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    def list_attribute_values(
        self,
        *,
        attribute_id: str,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Get attribute values.

        Args:
            attribute_id: Attribute ID
            **kwargs: Additional query parameters

        Returns:
            List of attribute value objects

        Example:
            ```python
            values = client.products.metadata.list_attribute_values(
                attribute_id="123"
            )
            ```
        """
        params: Dict[str, Any] = {
            "attributeId": attribute_id,
        }
        params.update(kwargs)

        return self._get(
            "/v1/product-attributes/attribute-values",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    def list_attribute_value_units(
        self,
        *,
        attribute_value_id: str,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Get attribute value units.

        Args:
            attribute_value_id: Attribute value ID
            **kwargs: Additional query parameters

        Returns:
            List of attribute unit objects

        Example:
            ```python
            units = client.products.metadata.list_attribute_value_units(
                attribute_value_id="456"
            )
            ```
        """
        params: Dict[str, Any] = {
            "attributeValueId": attribute_value_id,
        }
        params.update(kwargs)

        return self._get(
            "/v1/product-attributes/attribute-value-units",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    # Origin Areas
    def list_origin_areas(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Get origin areas (product origin locations).

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of origin area objects

        Example:
            ```python
            areas = client.products.metadata.list_origin_areas()
            ```
        """
        return self._get(
            "/v1/product-origin-areas",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def query_origin_areas(
        self,
        *,
        code: str,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Query origin areas by code.

        Args:
            code: Origin area code
            **kwargs: Additional query parameters

        Returns:
            List of origin area objects

        Example:
            ```python
            areas = client.products.metadata.query_origin_areas(code="01")
            ```
        """
        params: Dict[str, Any] = {
            "code": code,
        }
        params.update(kwargs)

        return self._get(
            "/v1/product-origin-areas/query",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    def list_sub_origin_areas(
        self,
        *,
        parent_code: str,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        Get sub origin areas.

        Args:
            parent_code: Parent origin area code
            **kwargs: Additional query parameters

        Returns:
            List of sub origin area objects

        Example:
            ```python
            sub_areas = client.products.metadata.list_sub_origin_areas(
                parent_code="01"
            )
            ```
        """
        params: Dict[str, Any] = {
            "parentCode": parent_code,
        }
        params.update(kwargs)

        return self._get(
            "/v1/product-origin-areas/sub-origin-areas",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    # Manufacturers
    def list_manufacturers(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List manufacturers.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of manufacturer objects

        Example:
            ```python
            manufacturers = client.products.metadata.list_manufacturers()
            ```
        """
        return self._get(
            "/v1/product-manufacturers",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    # Catalog Models
    def list_models(
        self,
        *,
        category_id: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """
        List catalog models.

        Args:
            category_id: Filter by category ID
            **kwargs: Additional query parameters

        Returns:
            List of catalog model objects

        Example:
            ```python
            models = client.products.metadata.list_models(
                category_id="50000000"
            )
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(category_id, NotGiven):
            params["categoryId"] = category_id

        params.update(kwargs)

        return self._get(
            "/v1/product-models",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    def get_model(
        self,
        model_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get catalog model by ID.

        Args:
            model_id: Model ID
            **kwargs: Additional query parameters

        Returns:
            Model object

        Example:
            ```python
            model = client.products.metadata.get_model("123")
            ```
        """
        return self._get(
            f"/v1/product-models/{model_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    # Size Types
    def list_size_types(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List size types.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of size type objects

        Example:
            ```python
            sizes = client.products.metadata.list_size_types()
            ```
        """
        return self._get(
            "/v1/product-sizes",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def get_size_type(
        self,
        size_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get size type by ID.

        Args:
            size_id: Size type ID
            **kwargs: Additional query parameters

        Returns:
            Size type object

        Example:
            ```python
            size = client.products.metadata.get_size_type("123")
            ```
        """
        return self._get(
            f"/v1/product-sizes/{size_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    # Fashion Models
    def list_fashion_models(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        List fashion models.

        Args:
            **kwargs: Additional query parameters

        Returns:
            List of fashion model objects

        Example:
            ```python
            models = client.products.metadata.list_fashion_models()
            ```
        """
        return self._get(
            "/v1/product-fashion-models",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    def create_fashion_model(
        self,
        *,
        name: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a fashion model.

        Args:
            name: Fashion model name
            **kwargs: Additional parameters

        Returns:
            Created fashion model

        Example:
            ```python
            model = client.products.metadata.create_fashion_model(
                name="Model Name"
            )
            ```
        """
        body: Dict[str, Any] = {
            "name": name,
        }
        body.update(kwargs)

        return self._post(
            "/v1/product-fashion-models",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def update_fashion_model(
        self,
        *,
        model_id: str,
        name: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update a fashion model.

        Args:
            model_id: Fashion model ID
            name: Fashion model name
            **kwargs: Additional parameters

        Returns:
            Updated fashion model

        Example:
            ```python
            model = client.products.metadata.update_fashion_model(
                model_id="123",
                name="Updated Name"
            )
            ```
        """
        body: Dict[str, Any] = {}

        if not isinstance(name, NotGiven):
            body["name"] = name

        body.update(kwargs)

        return self._put(
            f"/v1/product-fashion-models/{model_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    def delete_fashion_model(
        self,
        model_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Delete a fashion model.

        Args:
            model_id: Fashion model ID
            **kwargs: Additional parameters

        Returns:
            Deletion response

        Example:
            ```python
            result = client.products.metadata.delete_fashion_model("123")
            ```
        """
        return self._delete(
            f"/v1/product-fashion-models/{model_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )


class AsyncProductsMetadata(AsyncAPIResource):
    """Async products metadata sub-resource."""

    async def list_brands(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List all product brands."""
        return await self._get(
            "/v1/product-brands",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def list_attributes(
        self, *, category_id: str, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """Get category attributes."""
        params: Dict[str, Any] = {"categoryId": category_id}
        params.update(kwargs)
        return await self._get(
            "/v1/product-attributes/attributes",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    async def list_attribute_values(
        self, *, attribute_id: str, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """Get attribute values."""
        params: Dict[str, Any] = {"attributeId": attribute_id}
        params.update(kwargs)
        return await self._get(
            "/v1/product-attributes/attribute-values",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    async def list_attribute_value_units(
        self, *, attribute_value_id: str, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """Get attribute value units."""
        params: Dict[str, Any] = {"attributeValueId": attribute_value_id}
        params.update(kwargs)
        return await self._get(
            "/v1/product-attributes/attribute-value-units",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    async def list_origin_areas(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get origin areas."""
        return await self._get(
            "/v1/product-origin-areas",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def query_origin_areas(
        self, *, code: str, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """Query origin areas by code."""
        params: Dict[str, Any] = {"code": code}
        params.update(kwargs)
        return await self._get(
            "/v1/product-origin-areas/query",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    async def list_sub_origin_areas(
        self, *, parent_code: str, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """Get sub origin areas."""
        params: Dict[str, Any] = {"parentCode": parent_code}
        params.update(kwargs)
        return await self._get(
            "/v1/product-origin-areas/sub-origin-areas",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    async def list_manufacturers(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List manufacturers."""
        return await self._get(
            "/v1/product-manufacturers",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def list_models(
        self, *, category_id: str | NotGiven = not_given, **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """List catalog models."""
        params: Dict[str, Any] = {}
        if not isinstance(category_id, NotGiven):
            params["categoryId"] = category_id
        params.update(kwargs)
        return await self._get(
            "/v1/product-models",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": params},
        )

    async def get_model(self, model_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Get catalog model by ID."""
        return await self._get(
            f"/v1/product-models/{model_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    async def list_size_types(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List size types."""
        return await self._get(
            "/v1/product-sizes",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def get_size_type(self, size_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Get size type by ID."""
        return await self._get(
            f"/v1/product-sizes/{size_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )

    async def list_fashion_models(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """List fashion models."""
        return await self._get(
            "/v1/product-fashion-models",
            cast_to=List[Dict[str, Any]],  # type: ignore
            options={"params": kwargs},
        )

    async def create_fashion_model(
        self, *, name: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Create a fashion model."""
        body: Dict[str, Any] = {"name": name}
        body.update(kwargs)
        return await self._post(
            "/v1/product-fashion-models",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def update_fashion_model(
        self, *, model_id: str, name: str | NotGiven = not_given, **kwargs: Any
    ) -> Dict[str, Any]:
        """Update a fashion model."""
        body: Dict[str, Any] = {}
        if not isinstance(name, NotGiven):
            body["name"] = name
        body.update(kwargs)
        return await self._put(
            f"/v1/product-fashion-models/{model_id}",
            cast_to=dict,  # type: ignore
            body=body,
        )

    async def delete_fashion_model(
        self, model_id: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Delete a fashion model."""
        return await self._delete(
            f"/v1/product-fashion-models/{model_id}",
            cast_to=dict,  # type: ignore
            options={"params": kwargs},
        )
