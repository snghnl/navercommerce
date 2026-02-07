"""Product types for the Naver Commerce SDK."""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from ..._models import BaseModel


class ProductStatus(str, Enum):
    """Product status enumeration."""

    SALE = "SALE"
    SUSPENSION = "SUSPENSION"
    OUTOFSTOCK = "OUTOFSTOCK"
    CLOSE = "CLOSE"


class ProductImage(BaseModel):
    """Product image information."""

    url: str
    image_type: str | None = Field(None, alias="imageType")
    image_order: int | None = Field(None, alias="imageOrder")


class SaleInfo(BaseModel):
    """Product sale information."""

    sale_price: int = Field(alias="salePrice")
    stock_quantity: int | None = Field(None, alias="stockQuantity")
    sale_start_date: str | None = Field(None, alias="saleStartDate")
    sale_end_date: str | None = Field(None, alias="saleEndDate")


class DeliveryInfo(BaseModel):
    """Product delivery information."""

    delivery_fee: int | None = Field(None, alias="deliveryFee")
    delivery_method: str | None = Field(None, alias="deliveryMethod")
    delivery_company: str | None = Field(None, alias="deliveryCompany")


class Product(BaseModel):
    """
    Product information.

    This represents a complete product in the Naver Commerce system
    with all its attributes, pricing, and status information.
    """

    id: str
    name: str
    status: ProductStatus
    sale_price: int = Field(alias="salePrice")

    # Optional fields
    category_id: str | None = Field(None, alias="categoryId")
    category_name: str | None = Field(None, alias="categoryName")
    brand_id: str | None = Field(None, alias="brandId")
    brand_name: str | None = Field(None, alias="brandName")

    stock_quantity: int | None = Field(None, alias="stockQuantity")
    images: list[ProductImage] = Field(default_factory=list)

    origin_product_no: str | None = Field(None, alias="originProductNo")
    origin_area_code: str | None = Field(None, alias="originAreaCode")

    detail_content: str | None = Field(None, alias="detailContent")

    sale_info: SaleInfo | None = Field(None, alias="saleInfo")
    delivery_info: DeliveryInfo | None = Field(None, alias="deliveryInfo")

    created_date: str | None = Field(None, alias="createdDate")
    updated_date: str | None = Field(None, alias="updatedDate")

    # Additional fields that may be present in responses
    model_config = {"extra": "allow"}


class ProductList(BaseModel):
    """Paginated list of products."""

    contents: list[Product]
    total_count: int = Field(alias="totalCount")
    page: int
    size: int
