"""Order types for the Naver Commerce SDK."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from ..._models import BaseModel


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PAYMENT_WAITING = "PAYMENT_WAITING"
    PAYED = "PAYED"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    PURCHASE_DECIDED = "PURCHASE_DECIDED"
    EXCHANGED = "EXCHANGED"
    CANCELED = "CANCELED"
    RETURNED = "RETURNED"
    CANCELED_BY_NOPAYMENT = "CANCELED_BY_NOPAYMENT"


class ShippingInfo(BaseModel):
    """
    Shipping information for an order.

    Attributes:
        shipping_company: Shipping company name
        tracking_number: Tracking/invoice number
        shipping_date: Date when item was shipped
        delivery_method: Delivery method (DELIVERY, VISIT_RECEIPT, etc.)
    """

    shipping_company: Optional[str] = Field(None, alias="shippingCompany")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    shipping_date: Optional[str] = Field(None, alias="shippingDate")
    delivery_method: Optional[str] = Field(None, alias="deliveryMethod")


class OrdererInfo(BaseModel):
    """Information about the person who placed the order."""

    name: Optional[str] = None
    tel: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None


class ReceiverInfo(BaseModel):
    """Information about the order receiver."""

    name: Optional[str] = None
    tel: Optional[str] = Field(None, alias="tel1")
    mobile: Optional[str] = Field(None, alias="tel2")
    zip_code: Optional[str] = Field(None, alias="zipCode")
    address: Optional[str] = Field(None, alias="baseAddress")
    address_detail: Optional[str] = Field(None, alias="detailedAddress")


class OrderProductInfo(BaseModel):
    """
    Order product information.

    This represents a single product within an order.
    """

    product_order_id: str = Field(alias="productOrderId")
    order_id: str = Field(alias="orderId")
    product_id: str = Field(alias="productId")
    product_name: str = Field(alias="productName")

    product_option: Optional[str] = Field(None, alias="productOption")
    quantity: int = Field(default=1)
    unit_price: int = Field(alias="unitPrice")
    total_price: int = Field(alias="totalPrice")

    order_status: OrderStatus = Field(alias="productOrderStatus")
    claim_status: Optional[str] = Field(None, alias="claimStatus")

    order_date: Optional[str] = Field(None, alias="orderDate")
    payment_date: Optional[str] = Field(None, alias="paymentDate")

    shipping_info: Optional[ShippingInfo] = Field(None, alias="deliveryInfo")

    # Additional fields
    model_config = {"extra": "allow"}


class Order(BaseModel):
    """
    Complete order information.

    Represents a full order with all products, payment, and shipping details.
    """

    order_id: str = Field(alias="orderId")
    order_date: str = Field(alias="orderDate")

    order_status: Optional[str] = Field(None, alias="orderStatus")
    payment_date: Optional[str] = Field(None, alias="paymentDate")

    orderer: Optional[OrdererInfo] = Field(None, alias="orderer")
    receiver: Optional[ReceiverInfo] = Field(None, alias="shippingAddress")

    product_order_list: list[OrderProductInfo] = Field(default_factory=list, alias="productOrderList")

    total_product_price: Optional[int] = Field(None, alias="totalProductPrice")
    total_delivery_fee: Optional[int] = Field(None, alias="totalDeliveryFee")
    total_payment_amount: Optional[int] = Field(None, alias="totalPaymentAmount")

    # Additional fields
    model_config = {"extra": "allow"}


class OrderListResponse(BaseModel):
    """Response for order list queries."""

    contents: list[OrderProductInfo]
    total_count: int = Field(alias="totalCount")
    last: bool = Field(default=False)
