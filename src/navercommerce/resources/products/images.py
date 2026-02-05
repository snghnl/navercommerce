"""Product images resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.products import ProductImage

if TYPE_CHECKING:
    from ..._client import AsyncNaverCommerce, NaverCommerce
    from ..._types import FileTypes


class ProductImages(SyncAPIResource):
    """
    Product images resource for uploading product images.

    This resource provides methods to upload product images
    that can be used in product listings.
    """

    def upload(
        self,
        *,
        file: FileTypes,
        image_type: Literal["REPRESENTATIVE", "OPTIONAL"] = "OPTIONAL",
    ) -> ProductImage:
        """
        Upload a product image.

        Args:
            file: Image file to upload (bytes or file-like object)
            image_type: Type of image ("REPRESENTATIVE" for main image, "OPTIONAL" for additional)

        Returns:
            ProductImage object with URL and metadata

        Example:
            ```python
            # Upload from file path
            with open("product.jpg", "rb") as f:
                image = client.products.images.upload(
                    file=f.read(),
                    image_type="REPRESENTATIVE"
                )
                print(f"Image URL: {image.url}")

            # Upload with custom filename
            with open("product.jpg", "rb") as f:
                image = client.products.images.upload(
                    file=("product.jpg", f.read(), "image/jpeg"),
                    image_type="OPTIONAL"
                )
            ```
        """
        # Prepare multipart form data
        files = {"file": file}
        data = {"imageType": image_type}

        return self._post(
            "/v1/product-images",
            cast_to=ProductImage,
            files=files,
            body=data,
        )


class AsyncProductImages(AsyncAPIResource):
    """
    Async product images resource for uploading product images.

    This resource provides async methods to upload product images
    that can be used in product listings.
    """

    async def upload(
        self,
        *,
        file: FileTypes,
        image_type: Literal["REPRESENTATIVE", "OPTIONAL"] = "OPTIONAL",
    ) -> ProductImage:
        """
        Upload a product image asynchronously.

        Args:
            file: Image file to upload (bytes or file-like object)
            image_type: Type of image ("REPRESENTATIVE" for main image, "OPTIONAL" for additional)

        Returns:
            ProductImage object with URL and metadata

        Example:
            ```python
            # Upload from file path
            with open("product.jpg", "rb") as f:
                image = await client.products.images.upload(
                    file=f.read(),
                    image_type="REPRESENTATIVE"
                )
                print(f"Image URL: {image.url}")
            ```
        """
        # Prepare multipart form data
        files = {"file": file}
        data = {"imageType": image_type}

        return await self._post(
            "/v1/product-images",
            cast_to=ProductImage,
            files=files,
            body=data,
        )
