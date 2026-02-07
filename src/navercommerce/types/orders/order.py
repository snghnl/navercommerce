"""Order types for the Naver Commerce SDK."""

from __future__ import annotations

from enum import Enum

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

    shipping_company: str | None = Field(None, alias="shippingCompany")
    tracking_number: str | None = Field(None, alias="trackingNumber")
    shipping_date: str | None = Field(None, alias="shippingDate")
    delivery_method: str | None = Field(None, alias="deliveryMethod")


class OrdererInfo(BaseModel):
    """Information about the person who placed the order."""

    name: str | None = None
    tel: str | None = None
    mobile: str | None = None
    email: str | None = None


class ReceiverInfo(BaseModel):
    """Information about the order receiver."""

    name: str | None = None
    tel: str | None = Field(None, alias="tel1")
    mobile: str | None = Field(None, alias="tel2")
    zip_code: str | None = Field(None, alias="zipCode")
    address: str | None = Field(None, alias="baseAddress")
    address_detail: str | None = Field(None, alias="detailedAddress")


class OrderProductInfo(BaseModel):
    """
    Order product information.

    This represents a single product within an order.
    """

    product_order_id: str = Field(alias="productOrderId")
    order_id: str = Field(alias="orderId")
    product_id: str = Field(alias="productId")
    product_name: str = Field(alias="productName")

    product_option: str | None = Field(None, alias="productOption")
    quantity: int = Field(default=1)
    unit_price: int = Field(alias="unitPrice")
    total_price: int = Field(alias="totalPrice")

    order_status: OrderStatus = Field(alias="productOrderStatus")
    claim_status: str | None = Field(None, alias="claimStatus")

    order_date: str | None = Field(None, alias="orderDate")
    payment_date: str | None = Field(None, alias="paymentDate")

    shipping_info: ShippingInfo | None = Field(None, alias="deliveryInfo")

    # Additional fields
    model_config = {"extra": "allow"}


class Order(BaseModel):
    """
    Complete order information.

    Represents a full order with all products, payment, and shipping details.
    """

    order_id: str = Field(alias="orderId")
    order_date: str = Field(alias="orderDate")

    order_status: str | None = Field(None, alias="orderStatus")
    payment_date: str | None = Field(None, alias="paymentDate")

    orderer: OrdererInfo | None = Field(None, alias="orderer")
    receiver: ReceiverInfo | None = Field(None, alias="shippingAddress")

    product_order_list: list[OrderProductInfo] = Field(default_factory=list, alias="productOrderList")

    total_product_price: int | None = Field(None, alias="totalProductPrice")
    total_delivery_fee: int | None = Field(None, alias="totalDeliveryFee")
    total_payment_amount: int | None = Field(None, alias="totalPaymentAmount")

    # Additional fields
    model_config = {"extra": "allow"}


class OrderListResponse(BaseModel):
    """Response for order list queries."""

    contents: list[OrderProductInfo]
    total_count: int = Field(alias="totalCount")
    last: bool = Field(default=False)
