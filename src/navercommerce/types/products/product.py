"""Product types for the Naver Commerce SDK."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

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
    image_type: Optional[str] = Field(None, alias="imageType")
    image_order: Optional[int] = Field(None, alias="imageOrder")


class SaleInfo(BaseModel):
    """Product sale information."""

    sale_price: int = Field(alias="salePrice")
    stock_quantity: Optional[int] = Field(None, alias="stockQuantity")
    sale_start_date: Optional[str] = Field(None, alias="saleStartDate")
    sale_end_date: Optional[str] = Field(None, alias="saleEndDate")


class DeliveryInfo(BaseModel):
    """Product delivery information."""

    delivery_fee: Optional[int] = Field(None, alias="deliveryFee")
    delivery_method: Optional[str] = Field(None, alias="deliveryMethod")
    delivery_company: Optional[str] = Field(None, alias="deliveryCompany")


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
    category_id: Optional[str] = Field(None, alias="categoryId")
    category_name: Optional[str] = Field(None, alias="categoryName")
    brand_id: Optional[str] = Field(None, alias="brandId")
    brand_name: Optional[str] = Field(None, alias="brandName")

    stock_quantity: Optional[int] = Field(None, alias="stockQuantity")
    images: list[ProductImage] = Field(default_factory=list)

    origin_product_no: Optional[str] = Field(None, alias="originProductNo")
    origin_area_code: Optional[str] = Field(None, alias="originAreaCode")

    detail_content: Optional[str] = Field(None, alias="detailContent")

    sale_info: Optional[SaleInfo] = Field(None, alias="saleInfo")
    delivery_info: Optional[DeliveryInfo] = Field(None, alias="deliveryInfo")

    created_date: Optional[str] = Field(None, alias="createdDate")
    updated_date: Optional[str] = Field(None, alias="updatedDate")

    # Additional fields that may be present in responses
    model_config = {"extra": "allow"}


class ProductList(BaseModel):
    """Paginated list of products."""

    contents: list[Product]
    total_count: int = Field(alias="totalCount")
    page: int
    size: int
