"""Seller account types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..._models import BaseModel


class Account(BaseModel):
    """
    Seller account information.

    Attributes:
        seller_id: Unique seller identifier
        seller_name: Seller's business name
        tel_no: Seller's telephone number
        email: Seller's email address
        representative_name: Name of the business representative
        business_registration_no: Business registration number
    """

    seller_id: str = Field(alias="sellerId")
    seller_name: str = Field(alias="sellerName")
    tel_no: Optional[str] = Field(None, alias="telNo")
    email: Optional[str] = None
    representative_name: Optional[str] = Field(None, alias="representativeName")
    business_registration_no: Optional[str] = Field(None, alias="businessRegistrationNo")


class Channel(BaseModel):
    """
    Sales channel information.

    Attributes:
        channel_no: Unique channel identifier
        channel_name: Channel name
        is_default: Whether this is the default channel
    """

    channel_no: str = Field(alias="channelNo")
    channel_name: str = Field(alias="channelName")
    is_default: bool = Field(False, alias="isDefault")
