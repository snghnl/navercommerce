"""Products resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, List

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._types import NotGiven, not_given
from ...types.products import Brand, Category, Product

if TYPE_CHECKING:
    pass


class Products(SyncAPIResource):
    """
    Products resource for managing products, categories, and brands.

    This resource provides access to:
    - Product CRUD operations
    - Product categories
    - Product brands
    - Product image uploads (via images sub-resource)
    """

    @cached_property
    def images(self) -> Any:
        """
        Access the ProductImages subresource.

        Returns:
            ProductImages resource for uploading product images.

        Example:
            ```python
            with open("product.jpg", "rb") as f:
                image = client.products.images.upload(
                    file=f.read(),
                    image_type="REPRESENTATIVE"
                )
            ```
        """
        from .images import ProductImages

        return ProductImages(self._client)

    @cached_property
    def metadata(self) -> Any:
        """
        Access the Products Metadata sub-resource.

        Returns:
            ProductsMetadata resource for brands, attributes, origins, etc.

        Example:
            ```python
            brands = client.products.metadata.list_brands()
            ```
        """
        from .metadata import ProductsMetadata

        return ProductsMetadata(self._client)

    @cached_property
    def delivery(self) -> Any:
        """
        Access the Products Delivery sub-resource.

        Returns:
            ProductsDelivery resource for bundle groups, hope delivery, etc.

        Example:
            ```python
            groups = client.products.delivery.list_bundle_groups()
            ```
        """
        from .delivery import ProductsDelivery

        return ProductsDelivery(self._client)

    @cached_property
    def management(self) -> Any:
        """
        Access the Products Management sub-resource.

        Returns:
            ProductsManagement resource for bulk operations, status changes, etc.

        Example:
            ```python
            result = client.products.management.bulk_update(products=[...])
            ```
        """
        from .management import ProductsManagement

        return ProductsManagement(self._client)

    @cached_property
    def notices(self) -> Any:
        """
        Access the Products Notices sub-resource.

        Returns:
            ProductsNotices resource for product notice types.

        Example:
            ```python
            types = client.products.notices.list_types()
            ```
        """
        from .notices import ProductsNotices

        return ProductsNotices(self._client)

    def create(
        self,
        *,
        name: str,
        sale_price: int,
        category_id: str,
        origin_area_code: str,
        status: str | NotGiven = not_given,
        stock_quantity: int | NotGiven = not_given,
        brand_id: str | NotGiven = not_given,
        detail_content: str | NotGiven = not_given,
        images: List[Dict[str, Any]] | NotGiven = not_given,
        **kwargs: Any,
    ) -> Product:
        """
        Create a new product.

        Args:
            name: Product name
            sale_price: Sale price
            category_id: Category ID
            origin_area_code: Origin area code
            status: Product status (SALE, SUSPENSION, OUTOFSTOCK, CLOSE)
            stock_quantity: Stock quantity
            brand_id: Brand ID
            detail_content: Detailed product description (HTML)
            images: List of product images
            **kwargs: Additional product fields

        Returns:
            Created Product object

        Example:
            ```python
            product = client.products.create(
                name="Sample Product",
                sale_price=10000,
                category_id="50000000",
                origin_area_code="01",
                stock_quantity=100
            )
            print(f"Created product: {product.id}")
            ```
        """
        body: Dict[str, Any] = {
            "name": name,
            "salePrice": sale_price,
            "categoryId": category_id,
            "originAreaCode": origin_area_code,
        }

        if not isinstance(status, NotGiven):
            body["status"] = status
        if not isinstance(stock_quantity, NotGiven):
            body["stockQuantity"] = stock_quantity
        if not isinstance(brand_id, NotGiven):
            body["brandId"] = brand_id
        if not isinstance(detail_content, NotGiven):
            body["detailContent"] = detail_content
        if not isinstance(images, NotGiven):
            body["images"] = images

        body.update(kwargs)

        return self._post(
            "/v2/products",
            cast_to=Product,
            body=body,
        )

    def retrieve(self, product_id: str) -> Product:
        """
        Retrieve a product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product object

        Example:
            ```python
            product = client.products.retrieve("12345")
            print(f"Product: {product.name}")
            print(f"Price: {product.sale_price}")
            ```
        """
        return self._get(
            f"/v2/products/{product_id}",
            cast_to=Product,
        )

    def update(
        self,
        product_id: str,
        *,
        name: str | NotGiven = not_given,
        sale_price: int | NotGiven = not_given,
        status: str | NotGiven = not_given,
        stock_quantity: int | NotGiven = not_given,
        category_id: str | NotGiven = not_given,
        brand_id: str | NotGiven = not_given,
        detail_content: str | NotGiven = not_given,
        images: List[Dict[str, Any]] | NotGiven = not_given,
        **kwargs: Any,
    ) -> Product:
        """
        Update a product.

        Args:
            product_id: Product ID
            name: Product name
            sale_price: Sale price
            status: Product status
            stock_quantity: Stock quantity
            category_id: Category ID
            brand_id: Brand ID
            detail_content: Detailed product description
            images: List of product images
            **kwargs: Additional product fields

        Returns:
            Updated Product object

        Example:
            ```python
            product = client.products.update(
                "12345",
                name="Updated Product Name",
                sale_price=15000
            )
            ```
        """
        body: Dict[str, Any] = {}

        if not isinstance(name, NotGiven):
            body["name"] = name
        if not isinstance(sale_price, NotGiven):
            body["salePrice"] = sale_price
        if not isinstance(status, NotGiven):
            body["status"] = status
        if not isinstance(stock_quantity, NotGiven):
            body["stockQuantity"] = stock_quantity
        if not isinstance(category_id, NotGiven):
            body["categoryId"] = category_id
        if not isinstance(brand_id, NotGiven):
            body["brandId"] = brand_id
        if not isinstance(detail_content, NotGiven):
            body["detailContent"] = detail_content
        if not isinstance(images, NotGiven):
            body["images"] = images

        body.update(kwargs)

        return self._put(
            f"/v2/products/{product_id}",
            cast_to=Product,
            body=body,
        )

    def delete(self, product_id: str) -> None:
        """
        Delete a product.

        Args:
            product_id: Product ID

        Example:
            ```python
            client.products.delete("12345")
            ```
        """
        return self._delete(
            f"/v2/products/origin-products/{product_id}",
            cast_to=type(None),
        )

    def list(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Product]:
        """
        List products with pagination.

        Args:
            page: Page number (1-indexed)
            size: Number of items per page
            **kwargs: Additional query parameters

        Returns:
            List of Product objects

        Example:
            ```python
            products = client.products.list(page=1, size=20)
            for product in products:
                print(f"{product.name}: {product.sale_price}원")
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v2/products",
            cast_to=List[Product],  # type: ignore
            params=params,
        )

    def list_categories(
        self,
        *,
        parent_category_id: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Category]:
        """
        List product categories.

        Args:
            parent_category_id: Parent category ID (optional, for subcategories)
            **kwargs: Additional query parameters

        Returns:
            List of Category objects

        Example:
            ```python
            # Get root categories
            categories = client.products.list_categories()

            # Get subcategories
            subcategories = client.products.list_categories(
                parent_category_id="50000000"
            )
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(parent_category_id, NotGiven):
            params["parentCategoryId"] = parent_category_id

        params.update(kwargs)

        return self._get(
            "/v1/products/categories",
            cast_to=List[Category],  # type: ignore
            params=params,
        )

    def get_category(self, category_id: str) -> Category:
        """
        Get a specific category by ID.

        Args:
            category_id: Category ID

        Returns:
            Category object

        Example:
            ```python
            category = client.products.get_category("50000000")
            print(f"Category: {category.name}")
            ```
        """
        return self._get(
            f"/v1/products/categories/{category_id}",
            cast_to=Category,
        )

    def list_brands(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Brand]:
        """
        List product brands.

        Args:
            page: Page number (1-indexed)
            size: Number of items per page
            **kwargs: Additional query parameters

        Returns:
            List of Brand objects

        Example:
            ```python
            brands = client.products.list_brands(page=1, size=50)
            for brand in brands:
                print(f"Brand: {brand.name}")
            ```
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return self._get(
            "/v1/products/brands",
            cast_to=List[Brand],  # type: ignore
            params=params,
        )


class AsyncProducts(AsyncAPIResource):
    """
    Async products resource for managing products, categories, and brands.

    This resource provides async access to:
    - Product CRUD operations
    - Product categories
    - Product brands
    - Product image uploads (via images sub-resource)
    """

    @cached_property
    def images(self) -> Any:
        """
        Access the ProductImages subresource.

        Returns:
            AsyncProductImages resource for uploading product images.

        Example:
            ```python
            with open("product.jpg", "rb") as f:
                image = await client.products.images.upload(
                    file=f.read(),
                    image_type="REPRESENTATIVE"
                )
            ```
        """
        from .images import AsyncProductImages

        return AsyncProductImages(self._client)

    @cached_property
    def metadata(self) -> Any:
        """Access the async Products Metadata sub-resource."""
        from .metadata import AsyncProductsMetadata

        return AsyncProductsMetadata(self._client)

    @cached_property
    def delivery(self) -> Any:
        """Access the async Products Delivery sub-resource."""
        from .delivery import AsyncProductsDelivery

        return AsyncProductsDelivery(self._client)

    @cached_property
    def management(self) -> Any:
        """Access the async Products Management sub-resource."""
        from .management import AsyncProductsManagement

        return AsyncProductsManagement(self._client)

    @cached_property
    def notices(self) -> Any:
        """Access the async Products Notices sub-resource."""
        from .notices import AsyncProductsNotices

        return AsyncProductsNotices(self._client)

    async def create(
        self,
        *,
        name: str,
        sale_price: int,
        category_id: str,
        origin_area_code: str,
        status: str | NotGiven = not_given,
        stock_quantity: int | NotGiven = not_given,
        brand_id: str | NotGiven = not_given,
        detail_content: str | NotGiven = not_given,
        images: List[Dict[str, Any]] | NotGiven = not_given,
        **kwargs: Any,
    ) -> Product:
        """
        Create a new product.

        Args:
            name: Product name
            sale_price: Sale price
            category_id: Category ID
            origin_area_code: Origin area code
            status: Product status (SALE, SUSPENSION, OUTOFSTOCK, CLOSE)
            stock_quantity: Stock quantity
            brand_id: Brand ID
            detail_content: Detailed product description (HTML)
            images: List of product images
            **kwargs: Additional product fields

        Returns:
            Created Product object
        """
        body: Dict[str, Any] = {
            "name": name,
            "salePrice": sale_price,
            "categoryId": category_id,
            "originAreaCode": origin_area_code,
        }

        if not isinstance(status, NotGiven):
            body["status"] = status
        if not isinstance(stock_quantity, NotGiven):
            body["stockQuantity"] = stock_quantity
        if not isinstance(brand_id, NotGiven):
            body["brandId"] = brand_id
        if not isinstance(detail_content, NotGiven):
            body["detailContent"] = detail_content
        if not isinstance(images, NotGiven):
            body["images"] = images

        body.update(kwargs)

        return await self._post(
            "/v2/products",
            cast_to=Product,
            body=body,
        )

    async def retrieve(self, product_id: str) -> Product:
        """
        Retrieve a product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product object
        """
        return await self._get(
            f"/v2/products/{product_id}",
            cast_to=Product,
        )

    async def update(
        self,
        product_id: str,
        *,
        name: str | NotGiven = not_given,
        sale_price: int | NotGiven = not_given,
        status: str | NotGiven = not_given,
        stock_quantity: int | NotGiven = not_given,
        category_id: str | NotGiven = not_given,
        brand_id: str | NotGiven = not_given,
        detail_content: str | NotGiven = not_given,
        images: List[Dict[str, Any]] | NotGiven = not_given,
        **kwargs: Any,
    ) -> Product:
        """
        Update a product.

        Args:
            product_id: Product ID
            name: Product name
            sale_price: Sale price
            status: Product status
            stock_quantity: Stock quantity
            category_id: Category ID
            brand_id: Brand ID
            detail_content: Detailed product description
            images: List of product images
            **kwargs: Additional product fields

        Returns:
            Updated Product object
        """
        body: Dict[str, Any] = {}

        if not isinstance(name, NotGiven):
            body["name"] = name
        if not isinstance(sale_price, NotGiven):
            body["salePrice"] = sale_price
        if not isinstance(status, NotGiven):
            body["status"] = status
        if not isinstance(stock_quantity, NotGiven):
            body["stockQuantity"] = stock_quantity
        if not isinstance(category_id, NotGiven):
            body["categoryId"] = category_id
        if not isinstance(brand_id, NotGiven):
            body["brandId"] = brand_id
        if not isinstance(detail_content, NotGiven):
            body["detailContent"] = detail_content
        if not isinstance(images, NotGiven):
            body["images"] = images

        body.update(kwargs)

        return await self._put(
            f"/v2/products/{product_id}",
            cast_to=Product,
            body=body,
        )

    async def delete(self, product_id: str) -> None:
        """
        Delete a product.

        Args:
            product_id: Product ID
        """
        return await self._delete(
            f"/v2/products/origin-products/{product_id}",
            cast_to=type(None),
        )

    async def list(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Product]:
        """
        List products with pagination.

        Args:
            page: Page number (1-indexed)
            size: Number of items per page
            **kwargs: Additional query parameters

        Returns:
            List of Product objects
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v2/products",
            cast_to=List[Product],  # type: ignore
            params=params,
        )

    async def list_categories(
        self,
        *,
        parent_category_id: str | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Category]:
        """
        List product categories.

        Args:
            parent_category_id: Parent category ID (optional, for subcategories)
            **kwargs: Additional query parameters

        Returns:
            List of Category objects
        """
        params: Dict[str, Any] = {}

        if not isinstance(parent_category_id, NotGiven):
            params["parentCategoryId"] = parent_category_id

        params.update(kwargs)

        return await self._get(
            "/v1/products/categories",
            cast_to=List[Category],  # type: ignore
            params=params,
        )

    async def get_category(self, category_id: str) -> Category:
        """
        Get a specific category by ID.

        Args:
            category_id: Category ID

        Returns:
            Category object
        """
        return await self._get(
            f"/v1/products/categories/{category_id}",
            cast_to=Category,
        )

    async def list_brands(
        self,
        *,
        page: int | NotGiven = not_given,
        size: int | NotGiven = not_given,
        **kwargs: Any,
    ) -> List[Brand]:
        """
        List product brands.

        Args:
            page: Page number (1-indexed)
            size: Number of items per page
            **kwargs: Additional query parameters

        Returns:
            List of Brand objects
        """
        params: Dict[str, Any] = {}

        if not isinstance(page, NotGiven):
            params["page"] = page
        if not isinstance(size, NotGiven):
            params["size"] = size

        params.update(kwargs)

        return await self._get(
            "/v1/products/brands",
            cast_to=List[Brand],  # type: ignore
            params=params,
        )
